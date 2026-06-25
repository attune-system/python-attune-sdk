"""High-level helpers for action-owned Attune artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import quote

import httpx

from attune.client import AttuneClient
from attune.context import ActionContext, action_context


class ArtifactHelperError(RuntimeError):
    """Raised when action artifact helpers cannot complete safely."""


class _ArtifactClient(Protocol):
    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any: ...

    def post(self, path: str, *, json: Any = None) -> Any: ...


@dataclass(slots=True)
class ArtifactAllocation:
    """Allocated file-backed artifact version and local writable path."""

    artifact_id: int
    artifact_ref: str
    scope: str
    owner: str
    artifact_type: str
    visibility: str
    version_id: int
    version: int
    file_path: str
    absolute_path: Path
    execution: int | None = None
    content_type: str | None = None
    created_by: str | None = None
    meta: Any = None
    raw_version: dict[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        self.absolute_path.parent.mkdir(parents=True, exist_ok=True)

    def write_text(self, text: str, *, encoding: str = "utf-8") -> Path:
        """Write UTF-8 text to the allocated artifact path."""
        self.absolute_path.parent.mkdir(parents=True, exist_ok=True)
        self.absolute_path.write_text(text, encoding=encoding)
        return self.absolute_path

    def write_bytes(self, data: bytes) -> Path:
        """Write bytes to the allocated artifact path."""
        self.absolute_path.parent.mkdir(parents=True, exist_ok=True)
        self.absolute_path.write_bytes(data)
        return self.absolute_path

    def open(self, mode: str = "r", *args: Any, **kwargs: Any):
        """Open the allocated artifact path."""
        self.absolute_path.parent.mkdir(parents=True, exist_ok=True)
        return self.absolute_path.open(mode, *args, **kwargs)


@dataclass(slots=True)
class ProgressArtifact:
    """Convenience wrapper for an action-owned progress artifact."""

    artifact_id: int
    artifact_ref: str
    scope: str
    owner: str
    visibility: str
    artifact_type: str
    content_type: str | None = None
    name: str | None = None
    description: str | None = None
    data: Any = None
    raw_artifact: dict[str, Any] = field(default_factory=dict, repr=False)
    _client: _ArtifactClient = field(repr=False, compare=False, default=None)  # type: ignore[assignment]

    def append(self, entry: Any) -> ProgressArtifact:
        """Append a progress entry and refresh local metadata."""
        response = _call_post(
            self._client,
            f"/api/v1/artifacts/{self.artifact_id}/progress",
            json={"entry": entry},
            action=f"appending progress to '{self.artifact_ref}'",
        )
        artifact = _unwrap_response(response, f"appending progress to '{self.artifact_ref}'")
        if artifact.get("type") != "progress":
            raise ArtifactHelperError(
                f"Artifact '{self.artifact_ref}' is type {artifact.get('type')!r}, not 'progress'."
            )
        self.content_type = artifact.get("content_type")
        self.name = artifact.get("name")
        self.description = artifact.get("description")
        self.data = artifact.get("data")
        self.raw_artifact = artifact
        return self


__all__ = [
    "ArtifactAllocation",
    "ArtifactHelperError",
    "ProgressArtifact",
    "allocate_file_version",
    "create_progress",
]


def allocate_file_version(
    artifact_ref: str,
    *,
    artifact_type: str = "file_text",
    scope: str = "action",
    owner: str | None = None,
    created_by: str | None = None,
    execution: int | str | None = None,
    visibility: str = "private",
    retention_policy: str | None = None,
    retention_limit: int | None = None,
    name: str | None = None,
    description: str | None = None,
    content_type: str | None = None,
    meta: Any = None,
    client: _ArtifactClient | None = None,
    context: ActionContext | None = None,
) -> ArtifactAllocation:
    """Upsert an artifact by ref and allocate a file-backed version path."""
    ctx = context or action_context
    owner_ref = owner or _require_action_ref(ctx)
    creator = created_by or _require_action_ref(ctx)
    execution_id = _coerce_execution_id(execution, ctx)
    artifacts_dir = _resolve_artifacts_dir(ctx)
    artifact_client = _resolve_client(client, ctx)

    payload = {
        "scope": scope,
        "owner": owner_ref,
        "type": artifact_type,
        "visibility": visibility,
        "retention_policy": retention_policy,
        "retention_limit": retention_limit,
        "name": name,
        "description": description,
        "execution": execution_id,
        "content_type": content_type,
        "meta": meta,
        "created_by": creator,
    }
    response = _call_post(
        artifact_client,
        f"/api/v1/artifacts/ref/{quote(artifact_ref, safe='')}/versions/file",
        json={key: value for key, value in payload.items() if value is not None},
        action=f"allocating file-backed version for '{artifact_ref}'",
    )
    version_data = _unwrap_response(
        response,
        f"allocating file-backed version for '{artifact_ref}'",
    )

    file_path = version_data.get("file_path")
    if not isinstance(file_path, str) or not file_path.strip():
        raise ArtifactHelperError(
            f"Artifact version allocation for '{artifact_ref}' did not return a file_path."
        )

    absolute_path = _resolve_absolute_artifact_path(artifacts_dir, file_path)

    return ArtifactAllocation(
        artifact_id=_require_int(version_data, "artifact", artifact_ref),
        artifact_ref=artifact_ref,
        scope=scope,
        owner=owner_ref,
        artifact_type=artifact_type,
        visibility=visibility,
        version_id=_require_int(version_data, "id", artifact_ref),
        version=_require_int(version_data, "version", artifact_ref),
        file_path=file_path,
        absolute_path=absolute_path,
        execution=execution_id,
        content_type=version_data.get("content_type") or content_type,
        created_by=creator,
        meta=version_data.get("meta", meta),
        raw_version=version_data,
    )


def create_progress(
    artifact_ref: str,
    *,
    scope: str = "action",
    owner: str | None = None,
    visibility: str = "private",
    retention_policy: str | None = None,
    retention_limit: int | None = None,
    name: str | None = None,
    description: str | None = None,
    content_type: str | None = "application/json",
    data: Any = None,
    reuse_existing: bool = True,
    client: _ArtifactClient | None = None,
    context: ActionContext | None = None,
) -> ProgressArtifact:
    """Create or reuse a progress artifact with action-context defaults."""
    ctx = context or action_context
    owner_ref = owner or _require_action_ref(ctx)
    artifact_client = _resolve_client(client, ctx)
    payload = {
        "ref": artifact_ref,
        "scope": scope,
        "owner": owner_ref,
        "type": "progress",
        "visibility": visibility,
        "retention_policy": retention_policy,
        "retention_limit": retention_limit,
        "name": name,
        "description": description,
        "content_type": content_type,
        "data": data,
    }

    try:
        response = artifact_client.post(
            "/api/v1/artifacts",
            json={key: value for key, value in payload.items() if value is not None},
        )
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code != 409 or not reuse_existing:
            raise _artifact_request_error(
                f"creating progress artifact '{artifact_ref}'",
                exc,
            ) from exc
        response = _call_get(
            artifact_client,
            f"/api/v1/artifacts/ref/{quote(artifact_ref, safe='')}",
            action=f"loading existing progress artifact '{artifact_ref}'",
        )

    artifact = _unwrap_response(response, f"creating progress artifact '{artifact_ref}'")
    if artifact.get("type") != "progress":
        raise ArtifactHelperError(
            f"Artifact '{artifact_ref}' already exists with type {artifact.get('type')!r}, not 'progress'."
        )

    return ProgressArtifact(
        artifact_id=_require_int(artifact, "id", artifact_ref),
        artifact_ref=artifact_ref,
        scope=str(artifact.get("scope") or scope),
        owner=str(artifact.get("owner") or owner_ref),
        visibility=str(artifact.get("visibility") or visibility),
        artifact_type="progress",
        content_type=artifact.get("content_type"),
        name=artifact.get("name"),
        description=artifact.get("description"),
        data=artifact.get("data"),
        raw_artifact=artifact,
        _client=artifact_client,
    )


def _call_post(
    client: _ArtifactClient,
    path: str,
    *,
    json: Any,
    action: str,
) -> Any:
    try:
        return client.post(path, json=json)
    except httpx.HTTPStatusError as exc:
        raise _artifact_request_error(action, exc) from exc


def _call_get(client: _ArtifactClient, path: str, *, action: str) -> Any:
    try:
        return client.get(path)
    except httpx.HTTPStatusError as exc:
        raise _artifact_request_error(action, exc) from exc


def _resolve_client(
    client: _ArtifactClient | None,
    context: ActionContext,
) -> _ArtifactClient:
    if client is not None:
        return client
    if not context.api_token:
        raise ArtifactHelperError(
            "Artifact helpers require ATTUNE_API_TOKEN or an explicit authenticated client."
        )
    return AttuneClient(api_url=context.api_url, api_token=context.api_token)


def _require_action_ref(context: ActionContext) -> str:
    if context.action_ref:
        return context.action_ref
    raise ArtifactHelperError(
        "Artifact helpers require ATTUNE_ACTION / attune.context.action_ref. "
        "These helpers are intended to run inside an action execution."
    )


def _resolve_artifacts_dir(context: ActionContext) -> Path:
    if context.artifacts_dir is None:
        raise ArtifactHelperError(
            "Artifact helpers require ATTUNE_ARTIFACTS_DIR / attune.context.artifacts_dir "
            "to allocate local file paths."
        )
    return context.artifacts_dir.resolve(strict=False)


def _coerce_execution_id(
    execution: int | str | None,
    context: ActionContext,
) -> int | None:
    if execution is None:
        raw_value: int | str | None = context.execution_id or None
    else:
        raw_value = execution

    if raw_value is None:
        return None
    if isinstance(raw_value, int):
        return raw_value

    value = str(raw_value).strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ArtifactHelperError(
            f"Execution ID must be an integer, got {raw_value!r}."
        ) from exc


def _unwrap_response(response: Any, action: str) -> dict[str, Any]:
    if not isinstance(response, dict):
        raise ArtifactHelperError(
            f"Unexpected response while {action}: expected JSON object, got {type(response).__name__}."
        )

    payload = response.get("data", response)
    if not isinstance(payload, dict):
        rendered = json.dumps(response, default=str)
        raise ArtifactHelperError(
            f"Unexpected response while {action}: expected object payload, got {rendered}."
        )
    return payload


def _require_int(payload: dict[str, Any], key: str, artifact_ref: str) -> int:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ArtifactHelperError(
            f"Artifact helper response for '{artifact_ref}' is missing integer field '{key}'."
        )
    return value


def _resolve_absolute_artifact_path(artifacts_dir: Path, file_path: str) -> Path:
    candidate = (artifacts_dir / file_path).resolve(strict=False)
    if not candidate.is_relative_to(artifacts_dir):
        raise ArtifactHelperError(
            f"Artifact file_path '{file_path}' escapes ATTUNE_ARTIFACTS_DIR '{artifacts_dir}'."
        )
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate


def _artifact_request_error(message: str, exc: httpx.HTTPStatusError) -> ArtifactHelperError:
    detail = exc.response.text.strip() if exc.response is not None else ""
    if detail:
        return ArtifactHelperError(f"Failed while {message}: {exc.response.status_code} {detail}")
    return ArtifactHelperError(f"Failed while {message}: {exc}")

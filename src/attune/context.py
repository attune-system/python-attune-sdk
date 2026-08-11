"""
Execution context — module-level singletons providing access to environment
variables and execution metadata.

Action context values are computed once at import time. Sensor context values
are also built at import time, but managed-sensor auth can be resolved from a
mutable token source so long-running sensors can pick up runtime-driven token
rotation.

Usage::

    from attune.context import action_context
    # or
    import attune
    print(attune.context.execution_id)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from attune.api_client import AuthenticatedClient


def _parse_expiry_timestamp(raw: str | int | float | None) -> float | None:
    """Parse an expiry timestamp from unix seconds or ISO-8601."""
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        if raw <= 0:
            return None
        return float(raw)

    value = str(raw).strip()
    if not value:
        return None

    try:
        parsed = float(value)
        if parsed > 0:
            return parsed
    except ValueError:
        pass

    iso_value = value.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(iso_value)
    except ValueError:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


@dataclass(frozen=True)
class SensorTokenState:
    """Snapshot of managed sensor auth state."""

    token: str
    expires_at: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "token", self.token or "")
        if self.expires_at is not None and not str(self.expires_at).strip():
            object.__setattr__(self, "expires_at", None)

    @property
    def has_token(self) -> bool:
        """Whether a non-empty token is available."""
        return bool(self.token)

    @property
    def expires_at_epoch(self) -> float | None:
        """Expiry timestamp as unix seconds if parseable."""
        return _parse_expiry_timestamp(self.expires_at)

    def is_expiring_within(
        self, seconds: float, *, now_epoch: float | None = None
    ) -> bool:
        """Whether the token expires within ``seconds``."""
        exp = self.expires_at_epoch
        if exp is None:
            return False
        import time

        now = time.time() if now_epoch is None else now_epoch
        return now >= (exp - max(0.0, seconds))


class SensorTokenProvider(Protocol):
    """Resolves the current managed sensor token state."""

    def current_token_state(self) -> SensorTokenState:
        """Return the latest token snapshot."""


@dataclass(frozen=True)
class EnvSensorTokenProvider:
    """Environment-backed token provider with fallback to initial state."""

    initial_state: SensorTokenState
    token_env_var: str = "ATTUNE_API_TOKEN"
    expires_env_vars: tuple[str, ...] = (
        "ATTUNE_API_TOKEN_EXPIRES_AT",
        "ATTUNE_SENSOR_TOKEN_EXPIRES_AT",
    )

    def current_token_state(self) -> SensorTokenState:
        token = os.environ.get(self.token_env_var, self.initial_state.token) or ""
        expires_at = None
        for key in self.expires_env_vars:
            value = os.environ.get(key)
            if value:
                expires_at = value
                break
        if expires_at is None:
            expires_at = self.initial_state.expires_at
        return SensorTokenState(token=token, expires_at=expires_at)


@dataclass(frozen=True)
class FileSensorTokenProvider:
    """File-backed token provider for managed sensor token rotation."""

    state_path: Path
    fallback_state: SensorTokenState | None = None

    def current_token_state(self) -> SensorTokenState:
        try:
            return self._read_state()
        except Exception as exc:
            if self.fallback_state and self.fallback_state.has_token:
                return self.fallback_state
            raise RuntimeError(
                f"Unable to read sensor token state from {self.state_path}: {exc}"
            ) from exc

    def _read_state(self) -> SensorTokenState:
        if not self.state_path.exists():
            raise FileNotFoundError("state file does not exist")

        raw = self.state_path.read_text(encoding="utf-8")
        body = json.loads(raw)
        if not isinstance(body, dict):
            raise ValueError("state file JSON must be an object")

        token = ""
        for key in ("token", "api_token"):
            value = body.get(key)
            if isinstance(value, str) and value.strip():
                token = value
                break
        if not token:
            raise ValueError("state file does not contain a token")

        expires_at = None
        for key in ("expires_at", "token_expires_at"):
            value = body.get(key)
            if isinstance(value, str) and value.strip():
                expires_at = value
                break

        return SensorTokenState(token=token, expires_at=expires_at)


@dataclass(frozen=True)
class ActionContext:
    """Immutable context available during action execution.

    Attributes:
        action_ref: The action reference (e.g., ``mypack.deploy``).
        pack_ref: The pack reference (e.g., ``mypack``).
        execution_id: The execution database ID.
        api_url: The Attune API base URL.
        api_token: The execution-scoped API token (if permission sets were granted).
        artifacts_dir: Path to the shared artifact volume.
        runtime_envs_dir: Path to the runtime environments root.
        rule_ref: The rule reference (if triggered by a rule).
        trigger_ref: The trigger reference (if triggered by an event).
    """

    action_ref: str
    pack_ref: str
    execution_id: str
    api_url: str
    api_token: str | None
    artifacts_dir: Path | None
    runtime_envs_dir: Path | None
    rule_ref: str | None
    trigger_ref: str | None

    @property
    def has_api_token(self) -> bool:
        """Whether an execution-scoped API token is available."""
        return bool(self.api_token)

    @property
    def client(self) -> AuthenticatedClient:
        """Lazily constructed authenticated API client for this execution.

        Uses the execution-scoped token and API URL from the context.
        The client instance is cached for the lifetime of the process.

        Supports both sync and async usage with the same instance::

            from attune.api_client.api.packs import list_packs

            # Sync
            response = list_packs.sync(client=attune.context.client)

            # Async
            response = await list_packs.asyncio(client=attune.context.client)

        Raises:
            RuntimeError: If no API token is available in this execution context.
        """
        return _get_action_client(self)


@dataclass(frozen=True)
class SensorContext:
    """Immutable context available during sensor execution.

    Attributes:
        sensor_ref: The sensor reference (e.g., ``mypack.my_sensor``).
        sensor_id: The sensor database ID.
        api_url: The Attune API base URL.
        api_token: The sensor-scoped API token.
        notifier_ws_url: The notifier WebSocket URL for managed sensor lifecycle updates.
        allow_insecure_notifier_ws: Whether non-loopback plaintext WebSockets are allowed.
        log_level: The configured log level.
        pack_ref: The pack reference derived from sensor_ref.
    """

    sensor_ref: str
    sensor_id: str
    api_url: str
    api_token: str
    notifier_ws_url: str
    allow_insecure_notifier_ws: bool
    log_level: str
    pack_ref: str
    token_provider: SensorTokenProvider = field(repr=False, compare=False)
    token_reconnect_window_seconds: float = 30.0

    @property
    def config(self) -> dict[str, str]:
        """Caller-supplied ``ATTUNE_SENSOR_CONFIG_*`` values.

        The managed sensor service does not inject persisted sensor ``config``
        into child processes. Use per-rule ``trigger_params`` for managed rule
        configuration.
        """
        prefix = "ATTUNE_SENSOR_CONFIG_"
        return {
            k[len(prefix) :].lower(): v
            for k, v in os.environ.items()
            if k.startswith(prefix)
        }

    @property
    def client(self) -> AuthenticatedClient:
        """Lazily constructed authenticated API client for this sensor.

        Uses the sensor-scoped token and API URL from the context.
        The client instance is cached for the lifetime of the process.

        Supports both sync and async usage with the same instance::

            from attune.api_client.api.sensors import list_sensors

            # Sync
            response = list_sensors.sync(client=attune.sensor_context.client)

            # Async
            response = await list_sensors.asyncio(client=attune.sensor_context.client)
        """
        return _get_sensor_client(self)

    @property
    def current_token_state(self) -> SensorTokenState:
        """Current managed-sensor token state."""
        return self.token_provider.current_token_state()

    @property
    def current_api_token(self) -> str:
        """Current sensor-scoped API token (supports runtime rotation)."""
        return self.current_token_state.token

    def is_api_token_expiring_within(self, seconds: float | None = None) -> bool:
        """Whether the current sensor token is near expiry."""
        window = (
            self.token_reconnect_window_seconds
            if seconds is None
            else max(0.0, float(seconds))
        )
        return self.current_token_state.is_expiring_within(window)


def _build_action_context() -> ActionContext:
    """Build the action context from current environment variables."""
    artifacts = os.environ.get("ATTUNE_ARTIFACTS_DIR")
    runtime_envs = os.environ.get("ATTUNE_RUNTIME_ENVS_DIR")
    return ActionContext(
        action_ref=os.environ.get("ATTUNE_ACTION", ""),
        pack_ref=os.environ.get("ATTUNE_PACK_REF", ""),
        execution_id=os.environ.get("ATTUNE_EXEC_ID", ""),
        api_url=os.environ.get("ATTUNE_API_URL", "http://localhost:8080"),
        api_token=os.environ.get("ATTUNE_API_TOKEN"),
        artifacts_dir=Path(artifacts) if artifacts else None,
        runtime_envs_dir=Path(runtime_envs) if runtime_envs else None,
        rule_ref=os.environ.get("ATTUNE_RULE"),
        trigger_ref=os.environ.get("ATTUNE_TRIGGER"),
    )


def _build_sensor_context() -> SensorContext:
    """Build the sensor context from current environment variables."""
    initial_token = os.environ.get("ATTUNE_API_TOKEN", "")
    initial_expires_at = os.environ.get(
        "ATTUNE_API_TOKEN_EXPIRES_AT"
    ) or os.environ.get("ATTUNE_SENSOR_TOKEN_EXPIRES_AT")
    initial_state = SensorTokenState(token=initial_token, expires_at=initial_expires_at)
    token_provider: SensorTokenProvider = EnvSensorTokenProvider(
        initial_state=initial_state
    )
    token_state_path = os.environ.get("ATTUNE_SENSOR_TOKEN_STATE_PATH")
    if token_state_path:
        token_provider = FileSensorTokenProvider(
            state_path=Path(token_state_path),
            fallback_state=initial_state if initial_state.has_token else None,
        )

    reconnect_window_raw = os.environ.get(
        "ATTUNE_SENSOR_TOKEN_RECONNECT_WINDOW_SECONDS", "30"
    )
    try:
        token_reconnect_window_seconds = max(0.0, float(reconnect_window_raw))
    except ValueError:
        token_reconnect_window_seconds = 30.0

    sensor_ref = os.environ.get("ATTUNE_SENSOR_REF", "")
    parts = sensor_ref.split(".")
    pack_ref = parts[0] if len(parts) >= 2 else ""
    allow_insecure_notifier_ws = os.environ.get(
        "ATTUNE_ALLOW_INSECURE_NOTIFIER_WS", "false"
    ).strip().lower() in {"1", "true", "yes", "on"}
    return SensorContext(
        sensor_ref=sensor_ref,
        sensor_id=os.environ.get("ATTUNE_SENSOR_ID", "0"),
        api_url=os.environ.get("ATTUNE_API_URL", "http://localhost:8080"),
        api_token=initial_token,
        notifier_ws_url=os.environ.get(
            "ATTUNE_NOTIFIER_WS_URL", "ws://localhost:8081/ws"
        ),
        allow_insecure_notifier_ws=allow_insecure_notifier_ws,
        log_level=os.environ.get("ATTUNE_LOG_LEVEL", "info").upper(),
        pack_ref=pack_ref,
        token_provider=token_provider,
        token_reconnect_window_seconds=token_reconnect_window_seconds,
    )


# --- Lazy client singletons ---

_action_client: AuthenticatedClient | None = None
_sensor_client: AuthenticatedClient | None = None


def _get_action_client(ctx: ActionContext) -> AuthenticatedClient:
    """Return (or create) the cached action client."""
    global _action_client
    if _action_client is None:
        if not ctx.api_token:
            raise RuntimeError(
                "No API token available. The action must have execution permission "
                "sets configured to receive an API token."
            )
        from attune.api_client import AuthenticatedClient

        _action_client = AuthenticatedClient(
            base_url=ctx.api_url,
            token=ctx.api_token,
        )
    return _action_client


def _get_sensor_client(ctx: SensorContext) -> AuthenticatedClient:
    """Return (or create) the cached sensor client."""
    global _sensor_client
    token = ctx.current_api_token
    if not token:
        raise RuntimeError(
            "Managed sensor API token is unavailable. Set ATTUNE_API_TOKEN or "
            "provide a readable ATTUNE_SENSOR_TOKEN_STATE_PATH."
        )
    if _sensor_client is None:
        from attune.api_client import AuthenticatedClient

        _sensor_client = AuthenticatedClient(
            base_url=ctx.api_url,
            token=token,
        )
    else:
        _sync_authenticated_client_token(_sensor_client, token)
    return _sensor_client


def _sync_authenticated_client_token(client: AuthenticatedClient, token: str) -> None:
    """Update an existing generated client with a new bearer token."""
    if client.token == token:
        return

    client.token = token
    auth_header = f"{client.prefix} {token}" if client.prefix else token
    client._headers[client.auth_header_name] = auth_header  # type: ignore[attr-defined]

    sync_client = getattr(client, "_client", None)
    if sync_client is not None:
        sync_client.headers[client.auth_header_name] = auth_header

    async_client = getattr(client, "_async_client", None)
    if async_client is not None:
        async_client.headers[client.auth_header_name] = auth_header


#: Module-level action context singleton. Computed once at import time.
action_context: ActionContext = _build_action_context()

#: Module-level sensor context singleton. Computed once at import time.
sensor_context: SensorContext = _build_sensor_context()

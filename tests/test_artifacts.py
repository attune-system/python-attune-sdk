"""Tests for attune.artifacts helpers."""

from __future__ import annotations

import shutil
from pathlib import Path

import httpx
import pytest

from attune.artifacts import ArtifactHelperError, allocate_file_version, create_progress
from attune.context import ActionContext


class FakeArtifactClient:
    def __init__(self, *, post_responses=None, get_responses=None):
        self.post_responses = list(post_responses or [])
        self.get_responses = list(get_responses or [])
        self.calls: list[tuple[str, str, object]] = []

    def post(self, path: str, *, json=None):
        self.calls.append(("post", path, json))
        if not self.post_responses:
            raise AssertionError(f"Unexpected POST {path}")
        response = self.post_responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response

    def get(self, path: str, *, params=None):
        self.calls.append(("get", path, params))
        if not self.get_responses:
            raise AssertionError(f"Unexpected GET {path}")
        response = self.get_responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


@pytest.fixture
def artifact_workspace() -> Path:
    workspace = Path(__file__).resolve().parent / "_artifact_test_workspace"
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)
    try:
        yield workspace
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


@pytest.fixture
def action_context(artifact_workspace: Path) -> ActionContext:
    return ActionContext(
        action_ref="python_example.artifact_demo",
        pack_ref="python_example",
        execution_id="42",
        api_url="http://api.example.test",
        api_token="token-123",
        artifacts_dir=artifact_workspace / "artifacts",
        runtime_envs_dir=None,
        rule_ref=None,
        trigger_ref=None,
    )


class TestAllocateFileVersion:
    def test_defaults_to_action_context_and_writes_file(self, action_context: ActionContext):
        client = FakeArtifactClient(
            post_responses=[
                {
                    "data": {
                        "id": 7,
                        "artifact": 3,
                        "version": 2,
                        "content_type": "text/plain",
                        "file_path": "python_example/artifact_demo/logs/v2.txt",
                        "meta": {"kind": "log"},
                    }
                }
            ]
        )

        allocation = allocate_file_version(
            "python_example.artifact_demo.log",
            meta={"kind": "log"},
            client=client,
            context=action_context,
        )

        assert client.calls == [
            (
                "post",
                "/api/v1/artifacts/ref/python_example.artifact_demo.log/versions/file",
                {
                    "scope": "action",
                    "owner": "python_example.artifact_demo",
                    "type": "file_text",
                    "visibility": "private",
                    "execution": 42,
                    "meta": {"kind": "log"},
                    "created_by": "python_example.artifact_demo",
                },
            )
        ]
        assert allocation.artifact_id == 3
        assert allocation.version_id == 7
        assert allocation.version == 2
        assert (
            allocation.absolute_path
            == action_context.artifacts_dir.resolve(strict=False)
            / "python_example/artifact_demo/logs/v2.txt"
        )
        assert allocation.absolute_path.parent.is_dir()

        allocation.write_text("hello\n")
        assert allocation.absolute_path.read_text(encoding="utf-8") == "hello\n"

    def test_rejects_file_paths_outside_artifacts_dir(self, action_context: ActionContext):
        client = FakeArtifactClient(
            post_responses=[
                {
                    "data": {
                        "id": 7,
                        "artifact": 3,
                        "version": 2,
                        "file_path": "../escape.txt",
                    }
                }
            ]
        )

        with pytest.raises(ArtifactHelperError, match="escapes ATTUNE_ARTIFACTS_DIR"):
            allocate_file_version(
                "python_example.artifact_demo.log",
                client=client,
                context=action_context,
            )

    def test_requires_action_context_when_owner_defaults_are_needed(
        self,
        artifact_workspace: Path,
    ):
        context = ActionContext(
            action_ref="",
            pack_ref="",
            execution_id="",
            api_url="http://api.example.test",
            api_token="token-123",
            artifacts_dir=artifact_workspace / "artifacts",
            runtime_envs_dir=None,
            rule_ref=None,
            trigger_ref=None,
        )

        with pytest.raises(ArtifactHelperError, match="ATTUNE_ACTION"):
            allocate_file_version("python_example.artifact_demo.log", context=context)

    def test_requires_artifacts_dir(self):
        context = ActionContext(
            action_ref="python_example.artifact_demo",
            pack_ref="python_example",
            execution_id="42",
            api_url="http://api.example.test",
            api_token="token-123",
            artifacts_dir=None,
            runtime_envs_dir=None,
            rule_ref=None,
            trigger_ref=None,
        )

        with pytest.raises(ArtifactHelperError, match="ATTUNE_ARTIFACTS_DIR"):
            allocate_file_version("python_example.artifact_demo.log", context=context)


class TestCreateProgress:
    def test_creates_progress_and_appends_entries(self, action_context: ActionContext):
        client = FakeArtifactClient(
            post_responses=[
                {
                    "data": {
                        "id": 11,
                        "ref": "python_example.artifact_demo.progress",
                        "scope": "action",
                        "owner": "python_example.artifact_demo",
                        "type": "progress",
                        "visibility": "private",
                        "content_type": "application/json",
                        "data": [],
                    }
                },
                {
                    "data": {
                        "id": 11,
                        "ref": "python_example.artifact_demo.progress",
                        "scope": "action",
                        "owner": "python_example.artifact_demo",
                        "type": "progress",
                        "visibility": "private",
                        "content_type": "application/json",
                        "data": [{"message": "warming up", "percent": 10}],
                    }
                },
            ]
        )

        progress = create_progress(
            "python_example.artifact_demo.progress",
            client=client,
            context=action_context,
        )

        assert client.calls[0] == (
            "post",
            "/api/v1/artifacts",
            {
                "ref": "python_example.artifact_demo.progress",
                "scope": "action",
                "owner": "python_example.artifact_demo",
                "type": "progress",
                "visibility": "private",
                "content_type": "application/json",
            },
        )
        returned = progress.append({"message": "warming up", "percent": 10})
        assert returned is progress
        assert progress.artifact_id == 11
        assert progress.data == [{"message": "warming up", "percent": 10}]
        assert client.calls[1] == (
            "post",
            "/api/v1/artifacts/11/progress",
            {"entry": {"message": "warming up", "percent": 10}},
        )

    def test_reuses_existing_progress_artifact_on_conflict(
        self,
        action_context: ActionContext,
    ):
        request = httpx.Request("POST", "http://api.example.test/api/v1/artifacts")
        response = httpx.Response(409, request=request, text="already exists")
        conflict = httpx.HTTPStatusError(
            "conflict",
            request=request,
            response=response,
        )
        client = FakeArtifactClient(
            post_responses=[conflict],
            get_responses=[
                {
                    "data": {
                        "id": 12,
                        "ref": "python_example.artifact_demo.progress",
                        "scope": "action",
                        "owner": "python_example.artifact_demo",
                        "type": "progress",
                        "visibility": "private",
                        "data": [{"message": "started"}],
                    }
                }
            ],
        )

        progress = create_progress(
            "python_example.artifact_demo.progress",
            client=client,
            context=action_context,
        )

        assert progress.artifact_id == 12
        assert progress.data == [{"message": "started"}]
        assert client.calls == [
            (
                "post",
                "/api/v1/artifacts",
                {
                    "ref": "python_example.artifact_demo.progress",
                    "scope": "action",
                    "owner": "python_example.artifact_demo",
                    "type": "progress",
                    "visibility": "private",
                    "content_type": "application/json",
                },
            ),
            (
                "get",
                "/api/v1/artifacts/ref/python_example.artifact_demo.progress",
                None,
            ),
        ]

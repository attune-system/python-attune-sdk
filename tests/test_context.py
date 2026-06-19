"""Tests for attune.context module."""

import json
import os
from pathlib import Path

import pytest

from attune.context import (
    ActionContext,
    FileSensorTokenProvider,
    SensorContext,
    SensorTokenState,
    _build_action_context,
    _build_sensor_context,
)


class TestActionContext:
    def test_reads_env_vars(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_ACTION", "mypack.deploy")
        monkeypatch.setenv("ATTUNE_PACK_REF", "mypack")
        monkeypatch.setenv("ATTUNE_EXEC_ID", "123")
        monkeypatch.setenv("ATTUNE_API_URL", "http://api:8080")
        monkeypatch.setenv("ATTUNE_API_TOKEN", "jwt-token-here")
        monkeypatch.setenv("ATTUNE_ARTIFACTS_DIR", "/opt/attune/artifacts")

        ctx = _build_action_context()
        assert ctx.action_ref == "mypack.deploy"
        assert ctx.pack_ref == "mypack"
        assert ctx.execution_id == "123"
        assert ctx.api_url == "http://api:8080"
        assert ctx.api_token == "jwt-token-here"
        assert ctx.has_api_token is True
        assert str(ctx.artifacts_dir) == "/opt/attune/artifacts"

    def test_defaults_without_env(self, monkeypatch):
        monkeypatch.delenv("ATTUNE_ACTION", raising=False)
        monkeypatch.delenv("ATTUNE_PACK_REF", raising=False)
        monkeypatch.delenv("ATTUNE_EXEC_ID", raising=False)
        monkeypatch.delenv("ATTUNE_API_URL", raising=False)
        monkeypatch.delenv("ATTUNE_API_TOKEN", raising=False)
        monkeypatch.delenv("ATTUNE_ARTIFACTS_DIR", raising=False)

        ctx = _build_action_context()
        assert ctx.action_ref == ""
        assert ctx.api_url == "http://localhost:8080"
        assert ctx.has_api_token is False
        assert ctx.artifacts_dir is None

    def test_frozen_immutable(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_ACTION", "test")
        ctx = _build_action_context()
        with pytest.raises(Exception):  # FrozenInstanceError
            ctx.action_ref = "changed"


class TestSensorContext:
    def test_reads_env_vars(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_SENSOR_REF", "mypack.my_sensor")
        monkeypatch.setenv("ATTUNE_SENSOR_ID", "7")
        monkeypatch.setenv("ATTUNE_NOTIFIER_WS_URL", "ws://notifier:8081/ws")

        ctx = _build_sensor_context()
        assert ctx.sensor_ref == "mypack.my_sensor"
        assert ctx.sensor_id == "7"
        assert ctx.pack_ref == "mypack"
        assert ctx.notifier_ws_url == "ws://notifier:8081/ws"

    def test_config_from_env(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_SENSOR_REF", "test.sensor")
        monkeypatch.setenv("ATTUNE_SENSOR_CONFIG_INTERVAL", "10")
        monkeypatch.setenv("ATTUNE_SENSOR_CONFIG_TARGET_URL", "http://example.com")

        ctx = _build_sensor_context()
        config = ctx.config
        assert config["interval"] == "10"
        assert config["target_url"] == "http://example.com"

    def test_current_api_token_reloads_from_env(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-1")
        ctx = _build_sensor_context()
        assert ctx.current_api_token == "token-1"

        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-2")
        assert ctx.current_api_token == "token-2"

    def test_current_token_state_defaults_to_env_when_no_rotation_source(self, monkeypatch):
        monkeypatch.delenv("ATTUNE_SENSOR_TOKEN_STATE_PATH", raising=False)
        monkeypatch.setenv("ATTUNE_API_TOKEN", "env-token")
        monkeypatch.setenv("ATTUNE_API_TOKEN_EXPIRES_AT", "2030-01-01T00:00:00Z")

        ctx = _build_sensor_context()
        state = ctx.current_token_state
        assert state.token == "env-token"
        assert state.expires_at == "2030-01-01T00:00:00Z"

    def test_file_token_provider_reads_rotated_state(self, monkeypatch):
        state_path = "/opt/attune/runtime/sensor-token-state.json"
        monkeypatch.setenv("ATTUNE_API_TOKEN", "fallback-token")
        monkeypatch.setenv("ATTUNE_SENSOR_TOKEN_STATE_PATH", state_path)

        def fake_exists(self):
            return str(self) == state_path

        def fake_read_text(self, encoding="utf-8"):
            if str(self) != state_path:
                raise FileNotFoundError(str(self))
            return json.dumps(
                {
                    "token": "rotated-token",
                    "expires_at": "2026-12-31T00:00:00Z",
                }
            )

        monkeypatch.setattr("pathlib.Path.exists", fake_exists)
        monkeypatch.setattr("pathlib.Path.read_text", fake_read_text)

        ctx = _build_sensor_context()
        state = ctx.current_token_state
        assert state.token == "rotated-token"
        assert state.expires_at == "2026-12-31T00:00:00Z"

    def test_file_token_provider_fallback_state(self):
        provider = FileSensorTokenProvider(
            state_path=Path(os.path.join("/", "does-not-exist", "sensor-token-state.json")),
            fallback_state=SensorTokenState(token="fallback", expires_at="2026-01-01T00:00:00Z"),
        )
        state = provider.current_token_state()
        assert state.token == "fallback"
        assert state.expires_at == "2026-01-01T00:00:00Z"

    def test_file_token_provider_raises_without_fallback(self):
        provider = FileSensorTokenProvider(
            state_path=Path(os.path.join("/", "does-not-exist", "sensor-token-state.json")),
            fallback_state=None,
        )
        with pytest.raises(RuntimeError):
            provider.current_token_state()

    def test_token_state_handles_missing_or_invalid_expiry_metadata_safely(self):
        missing = SensorTokenState(token="token-1", expires_at=None)
        invalid = SensorTokenState(token="token-1", expires_at="not-a-timestamp")
        assert missing.expires_at_epoch is None
        assert invalid.expires_at_epoch is None
        assert missing.is_expiring_within(30, now_epoch=1.0) is False
        assert invalid.is_expiring_within(30, now_epoch=1.0) is False

    def test_sensor_context_client_updates_bearer_token(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-1")
        ctx = _build_sensor_context()
        client = ctx.client
        assert client.token == "token-1"

        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-2")
        same_client = ctx.client
        assert same_client is client
        assert same_client.token == "token-2"

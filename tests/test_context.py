"""Tests for attune.context module."""

import os

import pytest

from attune.context import ActionContext, SensorContext, _build_action_context, _build_sensor_context


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
        monkeypatch.setenv("ATTUNE_MQ_URL", "amqp://rabbit:5672")

        ctx = _build_sensor_context()
        assert ctx.sensor_ref == "mypack.my_sensor"
        assert ctx.sensor_id == "7"
        assert ctx.pack_ref == "mypack"
        assert ctx.mq_url == "amqp://rabbit:5672"

    def test_config_from_env(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_SENSOR_REF", "test.sensor")
        monkeypatch.setenv("ATTUNE_SENSOR_CONFIG_INTERVAL", "10")
        monkeypatch.setenv("ATTUNE_SENSOR_CONFIG_TARGET_URL", "http://example.com")

        ctx = _build_sensor_context()
        config = ctx.config
        assert config["interval"] == "10"
        assert config["target_url"] == "http://example.com"

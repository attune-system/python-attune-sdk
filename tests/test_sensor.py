"""Tests for attune.sensor module."""

import sys
import threading
import time
import types
from unittest.mock import MagicMock

import pytest

from attune.context import _build_sensor_context
from attune.sensor import AsyncPollingSensor, PollingSensor, RuleState, Sensor


class TestRuleState:
    def test_basic_construction(self):
        rule = RuleState(
            rule_id=1,
            rule_ref="mypack.my_rule",
            trigger_ref="mypack.my_trigger",
            trigger_params={"interval": 5},
        )
        assert rule.rule_id == 1
        assert rule.rule_ref == "mypack.my_rule"
        assert rule.trigger_params == {"interval": 5}
        assert rule.enabled is True


class TestSensorBase:
    def test_signal_sets_shutdown(self):
        sensor = Sensor()
        assert sensor.is_shutting_down is False
        sensor._handle_signal(2, None)  # SIGINT
        assert sensor.is_shutting_down is True

    def test_shutdown_method(self):
        sensor = Sensor()
        sensor.shutdown()
        assert sensor.is_shutting_down is True

    def test_bootstrap_rules_from_env(self, monkeypatch):
        monkeypatch.setenv(
            "ATTUNE_SENSOR_TRIGGERS",
            '[{"id": 1, "ref": "mypack.rule1", "trigger_ref": "mypack.trig", "config": {"interval": "3"}}]',
        )
        sensor = Sensor()
        sensor._bootstrap_rules()
        assert 1 in sensor.rules
        assert sensor.rules[1].rule_ref == "mypack.rule1"
        assert sensor.rules[1].trigger_params == {"interval": "3"}

    def test_bootstrap_empty_env(self, monkeypatch):
        monkeypatch.delenv("ATTUNE_SENSOR_TRIGGERS", raising=False)
        sensor = Sensor()
        sensor._bootstrap_rules()
        assert len(sensor.rules) == 0

    @pytest.mark.parametrize("status_field", ["active", "enabled"])
    def test_disabled_rule_created_does_not_activate(self, status_field):
        events = []

        class HookSensor(Sensor):
            def on_rule_created(self, rule):
                events.append(rule.rule_id)

        sensor = HookSensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 12,
                "rule_ref": "pack.disabled",
                "trigger_ref": "pack.trigger",
                status_field: False,
            }
        )

        assert sensor.rules[12].enabled is False
        assert events == []

    def test_rule_lifecycle_hooks_called(self):
        events = []

        class HookSensor(Sensor):
            def on_rule_created(self, rule):
                events.append(("created", rule.rule_id))

            def on_rule_disabled(self, rule):
                events.append(("disabled", rule.rule_id))

            def on_rule_deleted(self, rule):
                events.append(("deleted", rule.rule_id))

            def on_rule_updated(self, rule, old_params):
                events.append(("updated", rule.rule_id, old_params))

        sensor = HookSensor()

        # Create
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 10,
                "rule_ref": "pack.rule",
                "trigger_params": {"interval": 5},
            }
        )
        assert ("created", 10) in events

        # Update params
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 10,
                "rule_ref": "pack.rule",
                "trigger_params": {"interval": 10},
            }
        )
        assert ("updated", 10, {"interval": 5}) in events

        # Disable
        sensor._handle_rule_message(
            {
                "event_type": "rule.disabled",
                "rule_id": 10,
            }
        )
        assert ("disabled", 10) in events

        # Delete
        sensor._handle_rule_message(
            {
                "event_type": "rule.deleted",
                "rule_id": 10,
            }
        )
        assert ("deleted", 10) in events

    def test_handle_lifecycle_envelope_dispatches_notification_payload(self):
        events = []

        class HookSensor(Sensor):
            def on_rule_created(self, rule):
                events.append(("created", rule.rule_id, rule.trigger_ref))

        sensor = HookSensor()
        sensor._handle_lifecycle_envelope(
            {
                "type": "notification",
                "payload": {
                    "event_type": "rule.created",
                    "rule_id": 11,
                    "rule_ref": "pack.rule",
                    "trigger_ref": "pack.trigger",
                    "trigger_params": {"interval": 5},
                    "active": True,
                },
            }
        )

        assert events == [("created", 11, "pack.trigger")]

    def test_managed_trigger_refs_are_deduplicated(self):
        sensor = Sensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 1,
                "rule_ref": "pack.rule1",
                "trigger_ref": "pack.trigger",
                "trigger_params": {},
            }
        )
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 2,
                "rule_ref": "pack.rule2",
                "trigger_ref": "pack.trigger",
                "trigger_params": {},
            }
        )

        assert sensor._managed_trigger_refs() == ["pack.trigger"]

    def test_managed_trigger_refs_use_complete_environment_list(self, monkeypatch):
        monkeypatch.setenv(
            "ATTUNE_SENSOR_TRIGGER_TYPES", '["pack.beta", "pack.alpha", "pack.beta"]'
        )
        sensor = Sensor()

        assert sensor._managed_trigger_refs() == ["pack.alpha", "pack.beta"]

    def test_lifecycle_envelopes_cover_full_rule_lifecycle(self):
        events = []

        class HookSensor(Sensor):
            def on_rule_created(self, rule):
                events.append(("created", rule.rule_id))

            def on_rule_enabled(self, rule):
                events.append(("enabled", rule.rule_id))

            def on_rule_updated(self, rule, old_params):
                events.append(("updated", rule.rule_id, old_params))

            def on_rule_disabled(self, rule):
                events.append(("disabled", rule.rule_id))

            def on_rule_deleted(self, rule):
                events.append(("deleted", rule.rule_id))

        sensor = HookSensor()

        def envelope(event_type, **payload):
            sensor._handle_lifecycle_envelope(
                {
                    "type": "notification",
                    "payload": {
                        "event_type": event_type,
                        "rule_id": 21,
                        "rule_ref": "pack.rule",
                        "trigger_ref": "pack.trigger",
                        "trigger_params": payload.pop(
                            "trigger_params", {"interval": 5}
                        ),
                        "auth_mode": "full",
                        **payload,
                    },
                }
            )

        envelope("rule.created", active=True)
        envelope("rule.updated", trigger_params={"interval": 10}, active=True)
        envelope("rule.disabled", active=False)
        envelope("rule.enabled", trigger_params={"interval": 10}, active=True)
        envelope("rule.deleted", active=False)

        assert events == [
            ("created", 21),
            ("updated", 21, {"interval": 5}),
            ("disabled", 21),
            ("enabled", 21),
            ("deleted", 21),
        ]

    def test_deferred_lifecycle_refetches_omitted_rule_details(self):
        sensor = Sensor()
        response = MagicMock()
        response.json.return_value = {
            "data": {
                "id": 31,
                "ref": "pack.rule",
                "trigger_ref": "pack.trigger",
                "trigger_params": {"large": "value"},
                "enabled": True,
            }
        }
        sensor._http_client = MagicMock()
        sensor._http_client.get.return_value = response

        sensor._handle_lifecycle_envelope(
            {
                "type": "notification",
                "payload": {
                    "event_type": "rule.created",
                    "rule_id": 31,
                    "rule_ref": "pack.rule",
                    "trigger_ref": "pack.trigger",
                    "active": True,
                    "auth_mode": "deferred",
                },
            }
        )

        assert sensor.rules[31].trigger_params == {"large": "value"}
        sensor._http_client.get.assert_called_once_with("/api/v1/rules/pack.rule")

    def test_deferred_lifecycle_preserves_existing_state_when_refetch_fails(self):
        sensor = Sensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 32,
                "rule_ref": "pack.rule",
                "trigger_ref": "pack.trigger",
                "trigger_params": {"large": "existing"},
            }
        )
        sensor._http_client = MagicMock()
        sensor._http_client.get.side_effect = RuntimeError("unavailable")

        sensor._handle_lifecycle_envelope(
            {
                "type": "notification",
                "payload": {
                    "event_type": "rule.updated",
                    "rule_id": 32,
                    "rule_ref": "pack.rule",
                    "trigger_ref": "pack.trigger",
                    "active": True,
                    "auth_mode": "deferred",
                },
            }
        )

        assert sensor.rules[32].trigger_params == {"large": "existing"}


class TestPollingSensor:
    def test_poll_called_for_each_rule(self):
        poll_calls = []

        class TestSensor(PollingSensor):
            interval = 0.05

            def poll(self, rule):
                poll_calls.append(rule.rule_id)
                if len(poll_calls) >= 3:
                    self.shutdown()

        sensor = TestSensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 1,
                "rule_ref": "pack.rule1",
                "trigger_params": {"interval": "0.05"},
            }
        )
        sensor._run_lifecycle()
        assert len(poll_calls) >= 3
        assert all(rid == 1 for rid in poll_calls)

    def test_multiple_rules_poll_independently(self):
        polled_rules = set()

        class TestSensor(PollingSensor):
            interval = 0.05

            def poll(self, rule):
                polled_rules.add(rule.rule_id)
                if len(polled_rules) >= 2:
                    self.shutdown()

        sensor = TestSensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 1,
                "rule_ref": "pack.rule1",
                "trigger_params": {},
            }
        )
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 2,
                "rule_ref": "pack.rule2",
                "trigger_params": {},
            }
        )
        sensor._run_lifecycle()
        assert 1 in polled_rules
        assert 2 in polled_rules

    def test_rule_interval_override(self):
        sensor = PollingSensor()
        sensor.interval = 10.0
        rule = RuleState(rule_id=1, rule_ref="r", trigger_params={"interval": "2.5"})
        assert sensor._get_rule_interval(rule) == 2.5

    def test_rule_disabled_stops_polling(self):
        poll_count = 0

        class TestSensor(PollingSensor):
            interval = 0.05

            def poll(self, rule):
                nonlocal poll_count
                poll_count += 1

        sensor = TestSensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 1,
                "rule_ref": "pack.rule1",
                "trigger_params": {},
            }
        )
        # Let it poll a few times
        time.sleep(0.15)
        sensor._handle_rule_message({"event_type": "rule.disabled", "rule_id": 1})
        count_at_disable = poll_count
        time.sleep(0.15)
        # Should not have polled more after disable
        assert poll_count <= count_at_disable + 1  # allow 1 in-flight

    def test_rule_restart_waits_for_previous_poll_to_exit(self):
        entered_first_poll = threading.Event()
        release_first_poll = threading.Event()
        concurrent_polls = 0
        max_concurrent_polls = 0
        counter_lock = threading.Lock()

        class TestSensor(PollingSensor):
            interval = 60.0

            def poll(self, rule):
                nonlocal concurrent_polls, max_concurrent_polls
                with counter_lock:
                    concurrent_polls += 1
                    max_concurrent_polls = max(max_concurrent_polls, concurrent_polls)
                try:
                    if not entered_first_poll.is_set():
                        entered_first_poll.set()
                        release_first_poll.wait(timeout=2)
                    else:
                        self.shutdown()
                finally:
                    with counter_lock:
                        concurrent_polls -= 1

        sensor = TestSensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 1,
                "rule_ref": "pack.rule1",
                "trigger_params": {"interval": "60"},
            }
        )
        assert entered_first_poll.wait(timeout=1)

        updater = threading.Thread(
            target=lambda: sensor._handle_rule_message(
                {
                    "event_type": "rule.created",
                    "rule_id": 1,
                    "rule_ref": "pack.rule1",
                    "trigger_params": {"interval": "30"},
                }
            )
        )
        updater.start()
        time.sleep(0.1)

        assert max_concurrent_polls == 1

        release_first_poll.set()
        updater.join(timeout=2)
        sensor.cleanup()
        assert max_concurrent_polls == 1


class TestAsyncPollingSensor:
    def test_async_poll_called(self):
        poll_calls = []

        class TestSensor(AsyncPollingSensor):
            interval = 0.05

            async def poll(self, rule):
                poll_calls.append(rule.rule_id)
                if len(poll_calls) >= 3:
                    self.shutdown()

        sensor = TestSensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 1,
                "rule_ref": "pack.rule1",
                "trigger_params": {},
            }
        )
        sensor._run_lifecycle()
        assert len(poll_calls) >= 3

    def test_async_setup_and_cleanup(self):
        events = []

        class TestSensor(AsyncPollingSensor):
            interval = 0.05

            async def setup(self):
                events.append("setup")

            async def poll(self, rule):
                events.append("poll")
                self.shutdown()

            async def cleanup(self):
                events.append("cleanup")

        sensor = TestSensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 1,
                "rule_ref": "pack.rule1",
                "trigger_params": {},
            }
        )
        sensor._run_lifecycle()
        assert events[0] == "setup"
        assert "poll" in events
        assert events[-1] == "cleanup"


# ---------------------------------------------------------------------------
# HTTP client & emit tests
# ---------------------------------------------------------------------------


class TestSensorHttpClient:
    def test_http_client_lazy_initialized(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-a")
        sensor = Sensor()
        assert sensor._http_client is None
        client = sensor.http_client
        assert client is not None
        assert sensor._http_client is client

    def test_http_client_reused(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-a")
        sensor = Sensor()
        client1 = sensor.http_client
        client2 = sensor.http_client
        assert client1 is client2

    def test_rebuild_http_client(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-a")
        sensor = Sensor()
        client1 = sensor.http_client
        sensor._rebuild_http_client()
        client2 = sensor.http_client
        assert client1 is not client2

    def test_http_client_rebuilt_when_token_changes(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-a")
        sensor = Sensor()
        client1 = sensor.http_client

        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-b")
        client2 = sensor.http_client

        assert client1 is not client2
        assert client2.headers.get("Authorization") == "Bearer token-b"

    def test_lifecycle_websocket_uses_current_token(self, monkeypatch):
        class FakeWebSocket:
            def settimeout(self, timeout):
                self.timeout = timeout

            def close(self):
                pass

        calls: list[dict[str, object]] = []

        fake_ws_module = types.SimpleNamespace()

        def create_connection(url, timeout, header):
            calls.append({"url": url, "timeout": timeout, "header": list(header)})
            return FakeWebSocket()

        fake_ws_module.create_connection = create_connection
        monkeypatch.setitem(sys.modules, "websocket", fake_ws_module)

        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-a")
        sensor = Sensor()
        sensor._create_lifecycle_websocket()

        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-b")
        sensor._create_lifecycle_websocket()

        assert calls[0]["header"] == ["Authorization: Bearer token-a"]
        assert calls[1]["header"] == ["Authorization: Bearer token-b"]

    def test_lifecycle_reconnect_detects_token_rotation(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-a")
        sensor = Sensor()
        sensor._lifecycle_ws_token = "token-a"

        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-b")
        assert sensor._should_reconnect_lifecycle_websocket() is True

    def test_lifecycle_reconnect_is_safe_without_expiry_metadata(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-a")
        monkeypatch.delenv("ATTUNE_API_TOKEN_EXPIRES_AT", raising=False)
        monkeypatch.delenv("ATTUNE_SENSOR_TOKEN_EXPIRES_AT", raising=False)
        sensor = Sensor()
        sensor._lifecycle_ws_token = "token-a"
        assert sensor._should_reconnect_lifecycle_websocket() is False

    def test_managed_http_client_fails_clearly_without_token(self, monkeypatch):
        monkeypatch.delenv("ATTUNE_API_TOKEN", raising=False)
        monkeypatch.delenv("ATTUNE_SENSOR_TOKEN_STATE_PATH", raising=False)
        sensor = Sensor()

        with pytest.raises(
            RuntimeError, match="Managed sensor API token is unavailable"
        ):
            _ = sensor.http_client

    @pytest.mark.parametrize(
        "url",
        ["ws://localhost:8081/ws", "ws://127.0.0.1:8081/ws", "ws://[::1]:8081/ws"],
    )
    def test_insecure_loopback_notifier_urls_are_allowed(self, monkeypatch, url):
        monkeypatch.setenv("ATTUNE_NOTIFIER_WS_URL", url)
        monkeypatch.delenv("ATTUNE_ALLOW_INSECURE_NOTIFIER_WS", raising=False)
        sensor = Sensor()
        sensor.context = _build_sensor_context()

        sensor._validate_notifier_ws_url()

    def test_insecure_remote_notifier_url_is_rejected(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_NOTIFIER_WS_URL", "ws://notifier.internal:8081/ws")
        monkeypatch.delenv("ATTUNE_ALLOW_INSECURE_NOTIFIER_WS", raising=False)
        sensor = Sensor()
        sensor.context = _build_sensor_context()

        with pytest.raises(RuntimeError, match="Insecure notifier WebSocket"):
            sensor._validate_notifier_ws_url()

    def test_insecure_remote_notifier_url_can_be_explicitly_allowed(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_NOTIFIER_WS_URL", "ws://notifier.internal:8081/ws")
        monkeypatch.setenv("ATTUNE_ALLOW_INSECURE_NOTIFIER_WS", "true")
        sensor = Sensor()
        sensor.context = _build_sensor_context()

        sensor._validate_notifier_ws_url()


class TestSensorEmit:
    def _make_sensor(self):
        sensor = Sensor()
        return sensor

    def _mock_response(self, event_id=42):
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"data": {"id": event_id}}
        return resp

    def test_emit_returns_event_id(self):
        sensor = self._make_sensor()
        mock_client = MagicMock()
        mock_client.post.return_value = self._mock_response(event_id=99)
        sensor._http_client = mock_client

        result = sensor.emit({"temp": 100}, trigger_ref="mypack.trigger")
        assert result == 99

    def test_emit_fails_clearly_without_managed_token(self, monkeypatch):
        monkeypatch.delenv("ATTUNE_API_TOKEN", raising=False)
        monkeypatch.delenv("ATTUNE_SENSOR_TOKEN_STATE_PATH", raising=False)
        sensor = self._make_sensor()

        with pytest.raises(
            RuntimeError, match="Managed sensor API token is unavailable"
        ):
            sensor.emit({"temp": 100}, trigger_ref="mypack.trigger")

    def test_emit_posts_to_events_endpoint(self):
        sensor = self._make_sensor()
        mock_client = MagicMock()
        mock_client.post.return_value = self._mock_response()
        sensor._http_client = mock_client

        sensor.emit({"key": "val"}, trigger_ref="mypack.trigger")
        mock_client.post.assert_called_once()
        args, kwargs = mock_client.post.call_args
        assert args[0] == "/api/v1/events"
        assert kwargs["json"]["trigger_ref"] == "mypack.trigger"
        assert kwargs["json"]["payload"] == {"key": "val"}

    def test_emit_targets_numeric_i64_rule_by_default_with_exact_body(self):
        sensor = self._make_sensor()
        mock_client = MagicMock()
        mock_client.post.return_value = self._mock_response()
        sensor._http_client = mock_client

        rule = RuleState(
            rule_id=2**40,
            rule_ref="mypack.my_rule",
            trigger_ref="mypack.trig",
            trigger_params={},
        )
        sensor.emit({"data": 1}, rule=rule)

        body = mock_client.post.call_args[1]["json"]
        assert body == {
            "trigger_ref": "mypack.trig",
            "payload": {"data": 1},
            "source": sensor.context.sensor_ref,
            "trigger_instance_id": f"rule_{2**40}",
        }

    def test_emit_excludes_rule_ref_when_target_rule_false(self):
        sensor = self._make_sensor()
        mock_client = MagicMock()
        mock_client.post.return_value = self._mock_response()
        sensor._http_client = mock_client

        rule = RuleState(
            rule_id=5,
            rule_ref="mypack.my_rule",
            trigger_ref="mypack.trig",
            trigger_params={},
        )
        sensor.emit({"data": 1}, rule=rule, target_rule=False)

        body = mock_client.post.call_args[1]["json"]
        assert "rule_ref" not in body
        assert "trigger_instance_id" not in body

    def test_emit_uses_rule_trigger_ref(self):
        sensor = self._make_sensor()
        mock_client = MagicMock()
        mock_client.post.return_value = self._mock_response()
        sensor._http_client = mock_client

        rule = RuleState(
            rule_id=1,
            rule_ref="r",
            trigger_ref="mypack.special_trigger",
            trigger_params={},
        )
        sensor.emit({"x": 1}, rule=rule)

        body = mock_client.post.call_args[1]["json"]
        assert body["trigger_ref"] == "mypack.special_trigger"

    def test_emit_returns_none_on_http_error(self):
        import httpx

        sensor = self._make_sensor()
        mock_client = MagicMock()
        mock_client.post.side_effect = httpx.HTTPStatusError(
            "Server Error", request=MagicMock(), response=MagicMock()
        )
        sensor._http_client = mock_client

        result = sensor.emit({"x": 1}, trigger_ref="t")
        assert result is None

    def test_emit_reconnects_on_transport_error(self):
        import httpx

        sensor = self._make_sensor()
        mock_client = MagicMock()
        # First call raises transport error
        mock_client.post.side_effect = httpx.ConnectError("connection reset")
        sensor._http_client = mock_client

        # Patch _rebuild to install a working client
        success_resp = self._mock_response(event_id=77)

        def fake_rebuild():
            new_client = MagicMock()
            new_client.post.return_value = success_resp
            sensor._http_client = new_client

        sensor._rebuild_http_client = fake_rebuild

        result = sensor.emit({"x": 1}, trigger_ref="t")
        assert result == 77

    def test_emit_returns_none_when_reconnect_also_fails(self):
        import httpx

        sensor = self._make_sensor()
        mock_client = MagicMock()
        mock_client.post.side_effect = httpx.ConnectError("connection reset")
        sensor._http_client = mock_client

        def fake_rebuild():
            new_client = MagicMock()
            new_client.post.side_effect = httpx.ConnectError("still broken")
            sensor._http_client = new_client

        sensor._rebuild_http_client = fake_rebuild

        result = sensor.emit({"x": 1}, trigger_ref="t")
        assert result is None


class TestAsyncSensorEmit:
    def _make_sensor(self):
        sensor = AsyncPollingSensor()
        return sensor

    def _mock_response(self, event_id=42):
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"data": {"id": event_id}}
        return resp

    @pytest.mark.asyncio
    async def test_async_emit_returns_event_id(self):
        sensor = self._make_sensor()

        async def mock_post(*args, **kwargs):
            return self._mock_response(event_id=55)

        mock_client = MagicMock()
        mock_client.post = mock_post
        sensor._async_http_client = mock_client

        result = await sensor.async_emit({"temp": 100}, trigger_ref="mypack.trigger")
        assert result == 55

    @pytest.mark.asyncio
    async def test_async_emit_fails_clearly_without_managed_token(self, monkeypatch):
        monkeypatch.delenv("ATTUNE_API_TOKEN", raising=False)
        monkeypatch.delenv("ATTUNE_SENSOR_TOKEN_STATE_PATH", raising=False)
        sensor = self._make_sensor()

        with pytest.raises(
            RuntimeError, match="Managed sensor API token is unavailable"
        ):
            await sensor.async_emit({"temp": 100}, trigger_ref="mypack.trigger")

    @pytest.mark.asyncio
    async def test_async_emit_targets_numeric_i64_rule_by_default_with_exact_body(self):
        sensor = self._make_sensor()
        captured_body = {}

        async def mock_post(url, json=None):
            captured_body.update(json)
            return self._mock_response(event_id=10)

        mock_client = MagicMock()
        mock_client.post = mock_post
        sensor._async_http_client = mock_client

        rule = RuleState(
            rule_id=2**40,
            rule_ref="pack.rule",
            trigger_ref="pack.trig",
            trigger_params={},
        )
        result = await sensor.async_emit({"data": 1}, rule=rule)

        assert result == 10
        assert captured_body == {
            "trigger_ref": "pack.trig",
            "payload": {"data": 1},
            "source": sensor.context.sensor_ref,
            "trigger_instance_id": f"rule_{2**40}",
        }

    @pytest.mark.asyncio
    async def test_async_emit_excludes_rule_ref_when_target_rule_false(self):
        sensor = self._make_sensor()
        captured_body = {}

        async def mock_post(url, json=None):
            captured_body.update(json)
            return self._mock_response()

        mock_client = MagicMock()
        mock_client.post = mock_post
        sensor._async_http_client = mock_client

        rule = RuleState(
            rule_id=3, rule_ref="pack.rule", trigger_ref="pack.trig", trigger_params={}
        )
        await sensor.async_emit({"data": 1}, rule=rule, target_rule=False)

        assert "rule_ref" not in captured_body
        assert "trigger_instance_id" not in captured_body

    @pytest.mark.asyncio
    async def test_async_emit_reconnects_on_transport_error(self):
        import httpx

        sensor = self._make_sensor()

        async def failing_post(*args, **kwargs):
            raise httpx.ConnectError("connection lost")

        async def success_post(*args, **kwargs):
            return self._mock_response(event_id=88)

        mock_client = MagicMock()
        mock_client.post = failing_post
        sensor._async_http_client = mock_client

        async def fake_rebuild():
            new_client = MagicMock()
            new_client.post = success_post
            sensor._async_http_client = new_client

        sensor._rebuild_async_http_client = fake_rebuild

        result = await sensor.async_emit({"x": 1}, trigger_ref="t")
        assert result == 88

    @pytest.mark.asyncio
    async def test_async_emit_returns_none_on_http_error(self):
        import httpx

        sensor = self._make_sensor()

        async def error_post(*args, **kwargs):
            resp = MagicMock()
            resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Bad Request", request=MagicMock(), response=MagicMock()
            )
            return resp

        mock_client = MagicMock()
        mock_client.post = error_post
        sensor._async_http_client = mock_client

        result = await sensor.async_emit({"x": 1}, trigger_ref="t")
        assert result is None

    @pytest.mark.asyncio
    async def test_async_emit_returns_none_when_reconnect_also_fails(self):
        import httpx

        sensor = self._make_sensor()

        async def failing_post(*args, **kwargs):
            raise httpx.ConnectError("broken")

        mock_client = MagicMock()
        mock_client.post = failing_post
        sensor._async_http_client = mock_client

        async def fake_rebuild():
            new_client = MagicMock()
            new_client.post = failing_post
            sensor._async_http_client = new_client

        sensor._rebuild_async_http_client = fake_rebuild

        result = await sensor.async_emit({"x": 1}, trigger_ref="t")
        assert result is None


class TestHttpClientLifecycle:
    def test_sync_client_closed_on_lifecycle_end(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-a")

        class QuickSensor(Sensor):
            def run(self):
                # Access http_client to create it, then exit
                _ = self.http_client
                self.shutdown()

        sensor = QuickSensor()
        sensor._run_lifecycle()
        # Client should be closed and cleared
        assert sensor._http_client is None

    def test_async_client_closed_on_lifecycle_end(self, monkeypatch):
        monkeypatch.setenv("ATTUNE_API_TOKEN", "token-a")

        class QuickSensor(AsyncPollingSensor):
            interval = 0.05

            async def setup(self):
                # Access the client to create it
                _ = self.async_http_client

            async def poll(self, rule):
                self.shutdown()

        sensor = QuickSensor()
        sensor._handle_rule_message(
            {
                "event_type": "rule.created",
                "rule_id": 1,
                "rule_ref": "pack.rule1",
                "trigger_params": {},
            }
        )
        sensor._run_lifecycle()
        # Client should be closed and cleared
        assert sensor._async_http_client is None

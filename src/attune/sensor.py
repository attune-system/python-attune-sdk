"""
Sensor base classes — lifecycle management, rule change hooks, event emission,
signal handling, and polling helpers (synchronous and asynchronous).

Architecture
~~~~~~~~~~~~

Attune sensors are long-running processes. The platform delivers **rule
lifecycle events** via RabbitMQ (or ``ATTUNE_SENSOR_TRIGGERS`` env on
startup) so the sensor knows which rules are active and what parameters
they carry.

Class hierarchy::

    Sensor (base — custom event loops)
    ├── PollingSensor (synchronous polling in a thread-per-rule model)
    └── AsyncPollingSensor (asyncio polling with per-rule tasks)

Quick start — synchronous polling::

    import attune

    class TempSensor(attune.PollingSensor):
        def setup(self):
            self.interval = 5.0

        def poll(self, rule):
            temp = read_temp(rule.trigger_params.get("device"))
            if temp > 100:
                self.emit({"temperature": temp}, rule=rule)

    attune.run_sensor(TempSensor)

Quick start — async polling::

    import attune

    class ApiSensor(attune.AsyncPollingSensor):
        async def setup(self):
            import httpx
            self.http = httpx.AsyncClient()
            self.interval = 10.0

        async def poll(self, rule):
            resp = await self.http.get(rule.trigger_params["url"])
            if resp.status_code != 200:
                self.emit({"status": resp.status_code}, rule=rule)

        async def cleanup(self):
            await self.http.aclose()

    attune.run_sensor(ApiSensor)

Custom event loop (non-polling)::

    class FileTailSensor(attune.Sensor):
        def run(self):
            import time
            path = attune.sensor_context.config.get("watch_path", "/var/log/app.log")
            with open(path) as f:
                f.seek(0, 2)  # end of file
                while not self.is_shutting_down:
                    line = f.readline()
                    if line:
                        self.emit({"line": line.strip()})
                    else:
                        time.sleep(0.5)

    attune.run_sensor(FileTailSensor)
"""

import asyncio
import json
import logging
import os
import signal
import sys
import threading
from dataclasses import dataclass, field
from typing import Any

from attune.context import sensor_context

logger = logging.getLogger("attune.sensor")


# ---------------------------------------------------------------------------
# Rule representation
# ---------------------------------------------------------------------------


@dataclass
class RuleState:
    """Represents an active rule bound to this sensor.

    Attributes:
        rule_id: The rule database ID.
        rule_ref: The rule reference string (e.g., ``mypack.alert_rule``).
        trigger_ref: The trigger reference this rule is bound to.
        trigger_params: Per-rule trigger parameters (interval, query, etc.).
        enabled: Whether the rule is currently enabled.
    """

    rule_id: int
    rule_ref: str
    trigger_ref: str = ""
    trigger_params: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


# ---------------------------------------------------------------------------
# Base Sensor
# ---------------------------------------------------------------------------


class Sensor:
    """Base class for all Attune sensors.

    Provides:

    - **Signal handling** (SIGINT, SIGTERM) for graceful shutdown.
    - **Rule lifecycle hooks** called when rules are created, enabled,
      disabled, deleted, or have their parameters updated.
    - **Event emission** via the Attune API.
    - **Structured JSON logging** to stderr.
    - **Bootstrap** from ``ATTUNE_SENSOR_TRIGGERS`` environment variable
      (delivers initial active rules at process start).

    Subclasses should override :meth:`run` for custom event loops, or use
    :class:`PollingSensor` / :class:`AsyncPollingSensor` for polling patterns.
    """

    def __init__(self) -> None:
        self.context = sensor_context
        self._shutdown_event = threading.Event()
        self._rules: dict[int, RuleState] = {}
        self._rules_lock = threading.Lock()
        self._http_client: Any = None
        self._setup_logging()
        self.logger = logging.getLogger(
            f"attune.sensor.{self.context.sensor_ref}"
            if self.context.sensor_ref
            else "attune.sensor"
        )

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def _setup_logging(self) -> None:
        from pythonjsonlogger.json import JsonFormatter

        level = getattr(logging, self.context.log_level, logging.INFO)
        root = logging.getLogger()
        root.setLevel(level)

        # Clear existing handlers to avoid duplicates on re-init
        root.handlers.clear()

        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)
        formatter = JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            rename_fields={
                "asctime": "timestamp",
                "levelname": "level",
                "name": "logger",
            },
            static_fields={"sensor": self.context.sensor_ref},
        )
        handler.setFormatter(formatter)
        root.addHandler(handler)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def http_client(self) -> Any:
        """Lazy-initialized httpx.Client for API communication."""
        if self._http_client is None:
            self._http_client = self._create_http_client()
        return self._http_client

    def _create_http_client(self) -> Any:
        """Create a new httpx.Client instance."""
        try:
            import httpx
        except ImportError:
            raise ImportError(
                "The 'httpx' library is required for event emission. "
                "Install with: pip install attune[http]"
            )
        return httpx.Client(
            base_url=self.context.api_url,
            headers={
                "Authorization": f"Bearer {self.context.api_token}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

    def _rebuild_http_client(self) -> None:
        """Close the existing client and create a fresh one."""
        if self._http_client is not None:
            try:
                self._http_client.close()
            except Exception:
                pass
            self._http_client = None
        self._http_client = self._create_http_client()

    @property
    def config(self) -> dict[str, str]:
        """Sensor-level configuration from environment variables."""
        return self.context.config

    @property
    def is_shutting_down(self) -> bool:
        """Whether a shutdown signal has been received."""
        return self._shutdown_event.is_set()

    @property
    def rules(self) -> dict[int, RuleState]:
        """Active rules keyed by rule_id. Thread-safe snapshot."""
        with self._rules_lock:
            return dict(self._rules)

    # ------------------------------------------------------------------
    # Lifecycle hooks (override in subclasses)
    # ------------------------------------------------------------------

    def setup(self) -> None:
        """Called once before the main loop starts. Override to initialize resources."""

    def cleanup(self) -> None:
        """Called once during shutdown. Override to release resources."""

    def run(self) -> None:
        """Main sensor loop. Override for custom event-driven sensors.

        The default implementation simply waits for shutdown (suitable when
        all work is driven by rule lifecycle hooks).
        """
        while not self._shutdown_event.is_set():
            self._shutdown_event.wait(timeout=10)

    # ------------------------------------------------------------------
    # Rule lifecycle hooks (override in subclasses)
    # ------------------------------------------------------------------

    def on_rule_created(self, rule: RuleState) -> None:
        """Called when a new rule is created and enabled for this sensor.

        Override to start per-rule resources (timers, connections, etc.).
        """

    def on_rule_enabled(self, rule: RuleState) -> None:
        """Called when a previously disabled rule is re-enabled.

        Default implementation delegates to :meth:`on_rule_created`.
        """
        self.on_rule_created(rule)

    def on_rule_disabled(self, rule: RuleState) -> None:
        """Called when an active rule is disabled.

        Override to stop per-rule resources without fully tearing them down.
        """

    def on_rule_deleted(self, rule: RuleState) -> None:
        """Called when a rule is permanently deleted.

        Default implementation delegates to :meth:`on_rule_disabled`.
        """
        self.on_rule_disabled(rule)

    def on_rule_updated(self, rule: RuleState, old_params: dict[str, Any]) -> None:
        """Called when a rule's trigger parameters change.

        Override to restart per-rule resources with new configuration.
        The default implementation disables then re-enables the rule.

        Args:
            rule: The rule with updated trigger_params.
            old_params: The previous trigger_params dict.
        """
        self.on_rule_disabled(rule)
        self.on_rule_enabled(rule)

    # ------------------------------------------------------------------
    # Rule management (called by the MQ consumer or bootstrap)
    # ------------------------------------------------------------------

    def _handle_rule_message(self, message: dict[str, Any]) -> None:
        """Dispatch a rule lifecycle message from RabbitMQ."""
        event_type = message.get("event_type", "")
        rule_id = message.get("rule_id")
        if rule_id is None:
            return

        rule_id = int(rule_id)
        rule_ref = message.get("rule_ref", f"rule_{rule_id}")
        trigger_ref = message.get("trigger_ref") or message.get("trigger_type", "")
        trigger_params = message.get("trigger_params", {})

        if event_type in ("RuleCreated", "RuleEnabled"):
            rule = RuleState(
                rule_id=rule_id,
                rule_ref=rule_ref,
                trigger_ref=trigger_ref,
                trigger_params=trigger_params,
                enabled=True,
            )
            with self._rules_lock:
                existing = self._rules.get(rule_id)
                self._rules[rule_id] = rule

            if existing and existing.trigger_params != trigger_params:
                self.on_rule_updated(rule, existing.trigger_params)
            elif event_type == "RuleEnabled" and existing:
                self.on_rule_enabled(rule)
            else:
                self.on_rule_created(rule)

        elif event_type in ("RuleDisabled",):
            with self._rules_lock:
                rule = self._rules.get(rule_id)
                if rule:
                    rule.enabled = False
            if rule:
                self.on_rule_disabled(rule)

        elif event_type in ("RuleDeleted",):
            with self._rules_lock:
                rule = self._rules.pop(rule_id, None)
            if rule:
                self.on_rule_deleted(rule)

        elif event_type == "RuleUpdated":
            with self._rules_lock:
                existing = self._rules.get(rule_id)
                if existing:
                    old_params = dict(existing.trigger_params)
                    existing.trigger_params = trigger_params
                    rule = existing
                else:
                    rule = RuleState(
                        rule_id=rule_id,
                        rule_ref=rule_ref,
                        trigger_ref=trigger_ref,
                        trigger_params=trigger_params,
                        enabled=True,
                    )
                    self._rules[rule_id] = rule
                    old_params = {}
            if old_params != trigger_params:
                self.on_rule_updated(rule, old_params)

    def _bootstrap_rules(self) -> None:
        """Load initial active rules from ATTUNE_SENSOR_TRIGGERS env var."""
        raw = os.environ.get("ATTUNE_SENSOR_TRIGGERS", "[]")
        try:
            triggers = json.loads(raw)
        except json.JSONDecodeError:
            triggers = []

        if not isinstance(triggers, list):
            triggers = []

        for item in triggers:
            if not isinstance(item, dict):
                continue
            rule_id = item.get("id") or item.get("rule_id")
            if rule_id is None:
                continue
            self._handle_rule_message(
                {
                    "event_type": "RuleCreated",
                    "rule_id": rule_id,
                    "rule_ref": item.get(
                        "ref", item.get("rule_ref", f"rule_{rule_id}")
                    ),
                    "trigger_ref": item.get("trigger_ref", ""),
                    "trigger_params": item.get(
                        "config", item.get("trigger_params", {})
                    ),
                }
            )

    # ------------------------------------------------------------------
    # MQ consumer (optional — for sensors using RabbitMQ rule lifecycle)
    # ------------------------------------------------------------------

    def _start_mq_consumer(self) -> threading.Thread | None:
        """Start a background thread consuming rule lifecycle messages from RabbitMQ.

        Returns None if MQ is not configured.
        """
        mq_url = self.context.mq_url
        if not mq_url or mq_url == "amqp://localhost:5672":
            # Only start if explicitly configured
            env_set = os.environ.get("ATTUNE_MQ_URL")
            if not env_set:
                return None

        thread = threading.Thread(
            target=self._mq_consume_loop,
            name="mq-consumer",
            daemon=True,
        )
        thread.start()
        return thread

    def _mq_consume_loop(self) -> None:
        """Reconnecting MQ consumer loop. Runs in a daemon thread."""
        try:
            import pika
            import pika.exceptions
        except ImportError:
            self.logger.error(
                "pika library required for MQ rule lifecycle. Install with: pip install pika"
            )
            return

        queue_name = f"sensor.{self.context.sensor_ref}"
        routing_keys = [
            "rule.created",
            "rule.enabled",
            "rule.disabled",
            "rule.deleted",
            "rule.updated",
        ]

        while not self._shutdown_event.is_set():
            connection = None
            try:
                params = pika.URLParameters(self.context.mq_url)
                params.heartbeat = 30
                params.blocked_connection_timeout = 30
                connection = pika.BlockingConnection(params)
                channel = connection.channel()

                channel.exchange_declare(
                    exchange=self.context.mq_exchange,
                    exchange_type="topic",
                    durable=True,
                )
                channel.queue_declare(queue=queue_name, durable=True)
                for rk in routing_keys:
                    channel.queue_bind(
                        queue=queue_name,
                        exchange=self.context.mq_exchange,
                        routing_key=rk,
                    )

                self.logger.info("MQ connected", extra={"queue": queue_name})

                for method, _properties, body in channel.consume(
                    queue=queue_name, inactivity_timeout=1
                ):
                    if self._shutdown_event.is_set():
                        break
                    if method is None:
                        continue
                    try:
                        message = json.loads(body)
                        self._handle_rule_message(message)
                    except json.JSONDecodeError:
                        self.logger.warning("Invalid JSON in MQ message")
                    except Exception as exc:
                        self.logger.error("Error processing MQ message: %s", exc)
                    channel.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as exc:
                self.logger.warning("MQ connection error, retrying in 5s: %s", exc)
            finally:
                if connection and not connection.is_closed:
                    try:
                        connection.close()
                    except Exception:
                        pass

            self._shutdown_event.wait(timeout=5)

    # ------------------------------------------------------------------
    # Event emission
    # ------------------------------------------------------------------

    def emit(
        self,
        payload: dict[str, Any],
        *,
        rule: RuleState | None = None,
        trigger_ref: str | None = None,
        target_rule: bool = False,
    ) -> int | None:
        """Emit a sensor event via the Attune API.

        Args:
            payload: The event payload dictionary.
            rule: The rule context (used to derive trigger_ref and add source metadata).
            trigger_ref: Explicit trigger ref override. Falls back to rule's trigger_ref
                or the sensor ref.
            target_rule: When True and a rule is provided, include the rule_ref in the
                event so the executor only evaluates that specific rule instead of all
                rules matching the trigger.

        Returns:
            The event ID if successfully posted, or None on failure.
        """
        resolved_trigger_ref = (
            trigger_ref
            or (rule.trigger_ref if rule else None)
            or self.context.sensor_ref
        )

        body: dict[str, Any] = {
            "trigger_ref": resolved_trigger_ref,
            "payload": payload,
            "source": self.context.sensor_ref,
        }
        if rule:
            body["trigger_instance_id"] = f"rule_{rule.rule_ref}"
            if target_rule:
                body["rule_ref"] = rule.rule_ref

        try:
            resp = self.http_client.post("/api/v1/events", json=body)
            resp.raise_for_status()
            event_id = resp.json().get("data", {}).get("id")
            self.logger.debug(
                "Event emitted",
                extra={"trigger_ref": resolved_trigger_ref, "event_id": event_id},
            )
            return event_id
        except Exception as exc:
            import httpx

            if not isinstance(exc, httpx.TransportError):
                self.logger.error("Failed to emit event: %s", exc)
                return None
            # Connection lost — rebuild client and retry once
            self.logger.warning("Transport error, reconnecting: %s", exc)
            try:
                self._rebuild_http_client()
                resp = self.http_client.post("/api/v1/events", json=body)
                resp.raise_for_status()
                event_id = resp.json().get("data", {}).get("id")
                self.logger.debug(
                    "Event emitted after reconnect",
                    extra={"trigger_ref": resolved_trigger_ref, "event_id": event_id},
                )
                return event_id
            except Exception as retry_exc:
                self.logger.error("Failed to emit event after reconnect: %s", retry_exc)
                return None

    # ------------------------------------------------------------------
    # Signal handling
    # ------------------------------------------------------------------

    def _handle_signal(self, signum: int, frame: Any) -> None:
        sig_name = (
            signal.Signals(signum).name if hasattr(signal, "Signals") else str(signum)
        )
        self.logger.info("Received %s, shutting down", sig_name)
        self._shutdown_event.set()

    def shutdown(self) -> None:
        """Programmatically request sensor shutdown."""
        self._shutdown_event.set()

    # ------------------------------------------------------------------
    # Main lifecycle
    # ------------------------------------------------------------------

    def _run_lifecycle(self) -> int:
        """Execute the full sensor lifecycle."""
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        mq_thread = None
        try:
            self._bootstrap_rules()
            self.setup()
            mq_thread = self._start_mq_consumer()
            self.logger.info("Sensor started", extra={"active_rules": len(self._rules)})
            self.run()
        except Exception as exc:
            self.logger.error("Sensor error: %s", exc)
            return 1
        finally:
            self._shutdown_event.set()
            try:
                self.cleanup()
            except Exception as exc:
                self.logger.error("Cleanup error: %s", exc)
            if self._http_client is not None:
                self._http_client.close()
                self._http_client = None
            if mq_thread:
                mq_thread.join(timeout=5)
            self.logger.info("Sensor stopped")

        return 0


# ---------------------------------------------------------------------------
# PollingSensor — synchronous, thread-per-rule polling
# ---------------------------------------------------------------------------


class PollingSensor(Sensor):
    """Sensor that polls on a fixed interval for each active rule.

    Uses one background thread per active rule. Override :meth:`poll` to
    implement the per-rule check logic.

    Attributes:
        interval: Default polling interval in seconds. Can be overridden
            per-rule via ``trigger_params["interval"]`` or
            ``trigger_params["interval_seconds"]``.
    """

    interval: float = 5.0

    def __init__(self) -> None:
        super().__init__()
        self._poll_threads: dict[int, threading.Event] = {}

    def poll(self, rule: RuleState) -> None:
        """Called periodically for each active rule.

        Override this to check for events and call :meth:`emit`.

        Args:
            rule: The rule being polled, including its trigger_params.
        """

    def _get_rule_interval(self, rule: RuleState) -> float:
        """Resolve the polling interval for a rule."""
        params = rule.trigger_params
        for key in ("interval", "interval_seconds", "poll_interval"):
            val = params.get(key)
            if val is not None:
                try:
                    return float(val)
                except (TypeError, ValueError):
                    pass
        return self.interval

    def _poll_loop(self, rule_id: int, stop_event: threading.Event) -> None:
        """Per-rule polling loop running in a dedicated thread."""
        while not stop_event.is_set() and not self._shutdown_event.is_set():
            with self._rules_lock:
                rule = self._rules.get(rule_id)
            if rule is None or not rule.enabled:
                break
            try:
                self.poll(rule)
            except Exception as exc:
                self.logger.error("Poll error for rule %s: %s", rule.rule_ref, exc)
            interval = self._get_rule_interval(rule)
            stop_event.wait(timeout=interval)

    def _start_poll_thread(self, rule: RuleState) -> None:
        """Start a polling thread for the given rule."""
        self._stop_poll_thread(rule.rule_id)
        stop_event = threading.Event()
        self._poll_threads[rule.rule_id] = stop_event
        thread = threading.Thread(
            target=self._poll_loop,
            args=(rule.rule_id, stop_event),
            name=f"poll-{rule.rule_ref}",
            daemon=True,
        )
        thread.start()

    def _stop_poll_thread(self, rule_id: int) -> None:
        """Stop the polling thread for a rule."""
        stop_event = self._poll_threads.pop(rule_id, None)
        if stop_event:
            stop_event.set()

    # Rule lifecycle hooks — start/stop polling threads

    def on_rule_created(self, rule: RuleState) -> None:
        self._start_poll_thread(rule)

    def on_rule_enabled(self, rule: RuleState) -> None:
        self._start_poll_thread(rule)

    def on_rule_disabled(self, rule: RuleState) -> None:
        self._stop_poll_thread(rule.rule_id)

    def on_rule_deleted(self, rule: RuleState) -> None:
        self._stop_poll_thread(rule.rule_id)

    def on_rule_updated(self, rule: RuleState, old_params: dict[str, Any]) -> None:
        # Restart the poll thread with new params
        self._start_poll_thread(rule)

    def run(self) -> None:
        """Wait for shutdown while poll threads handle per-rule work."""
        while not self._shutdown_event.is_set():
            self._shutdown_event.wait(timeout=10)

    def cleanup(self) -> None:
        """Stop all polling threads."""
        for rule_id in list(self._poll_threads.keys()):
            self._stop_poll_thread(rule_id)


# ---------------------------------------------------------------------------
# AsyncPollingSensor — asyncio-based, task-per-rule polling
# ---------------------------------------------------------------------------


class AsyncPollingSensor(Sensor):
    """Sensor that polls asynchronously using asyncio for each active rule.

    Uses one asyncio task per active rule within a single event loop.
    Override :meth:`poll` (async) to implement the per-rule check logic.

    Attributes:
        interval: Default polling interval in seconds.
    """

    interval: float = 5.0

    def __init__(self) -> None:
        super().__init__()
        self._poll_tasks: dict[int, asyncio.Task] = {}
        self._loop: asyncio.AbstractEventLoop | None = None
        self._async_http_client: Any = None

    async def poll(self, rule: RuleState) -> None:
        """Called periodically for each active rule (async).

        Override this to check for events and call :meth:`emit`.
        """

    async def setup(self) -> None:  # type: ignore[override]
        """Async setup — called once before the main loop."""

    async def cleanup(self) -> None:  # type: ignore[override]
        """Async cleanup — called once during shutdown."""

    @property
    def async_http_client(self) -> Any:
        """Lazy-initialized httpx.AsyncClient for API communication."""
        if self._async_http_client is None:
            self._async_http_client = self._create_async_http_client()
        return self._async_http_client

    def _create_async_http_client(self) -> Any:
        """Create a new httpx.AsyncClient instance."""
        try:
            import httpx
        except ImportError:
            raise ImportError(
                "The 'httpx' library is required for event emission. "
                "Install with: pip install attune[http]"
            )
        return httpx.AsyncClient(
            base_url=self.context.api_url,
            headers={
                "Authorization": f"Bearer {self.context.api_token}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

    async def _rebuild_async_http_client(self) -> None:
        """Close the existing async client and create a fresh one."""
        if self._async_http_client is not None:
            try:
                await self._async_http_client.aclose()
            except Exception:
                pass
            self._async_http_client = None
        self._async_http_client = self._create_async_http_client()

    async def async_emit(
        self,
        payload: dict[str, Any],
        *,
        rule: RuleState | None = None,
        trigger_ref: str | None = None,
        target_rule: bool = False,
    ) -> int | None:
        """Emit a sensor event via the Attune API (async).

        Args:
            payload: The event payload dictionary.
            rule: The rule context (used to derive trigger_ref and add source metadata).
            trigger_ref: Explicit trigger ref override. Falls back to rule's trigger_ref
                or the sensor ref.
            target_rule: When True and a rule is provided, include the rule_ref in the
                event so the executor only evaluates that specific rule instead of all
                rules matching the trigger.

        Returns:
            The event ID if successfully posted, or None on failure.
        """
        resolved_trigger_ref = (
            trigger_ref
            or (rule.trigger_ref if rule else None)
            or self.context.sensor_ref
        )

        body: dict[str, Any] = {
            "trigger_ref": resolved_trigger_ref,
            "payload": payload,
            "source": self.context.sensor_ref,
        }
        if rule:
            body["trigger_instance_id"] = f"rule_{rule.rule_ref}"
            if target_rule:
                body["rule_ref"] = rule.rule_ref

        try:
            resp = await self.async_http_client.post("/api/v1/events", json=body)
            resp.raise_for_status()
            event_id = resp.json().get("data", {}).get("id")
            self.logger.debug(
                "Event emitted",
                extra={"trigger_ref": resolved_trigger_ref, "event_id": event_id},
            )
            return event_id
        except Exception as exc:
            import httpx

            if not isinstance(exc, httpx.TransportError):
                self.logger.error("Failed to emit event: %s", exc)
                return None
            # Connection lost — rebuild client and retry once
            self.logger.warning("Transport error, reconnecting: %s", exc)
            try:
                await self._rebuild_async_http_client()
                resp = await self.async_http_client.post("/api/v1/events", json=body)
                resp.raise_for_status()
                event_id = resp.json().get("data", {}).get("id")
                self.logger.debug(
                    "Event emitted after reconnect",
                    extra={"trigger_ref": resolved_trigger_ref, "event_id": event_id},
                )
                return event_id
            except Exception as retry_exc:
                self.logger.error("Failed to emit event after reconnect: %s", retry_exc)
                return None

    def _get_rule_interval(self, rule: RuleState) -> float:
        """Resolve the polling interval for a rule."""
        params = rule.trigger_params
        for key in ("interval", "interval_seconds", "poll_interval"):
            val = params.get(key)
            if val is not None:
                try:
                    return float(val)
                except (TypeError, ValueError):
                    pass
        return self.interval

    async def _poll_task(self, rule_id: int) -> None:
        """Per-rule async polling task."""
        while not self._shutdown_event.is_set():
            with self._rules_lock:
                rule = self._rules.get(rule_id)
            if rule is None or not rule.enabled:
                break
            try:
                await self.poll(rule)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                self.logger.error("Poll error for rule %s: %s", rule.rule_ref, exc)
            interval = self._get_rule_interval(rule)
            try:
                await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(
                        None, self._shutdown_event.wait, interval
                    ),
                    timeout=interval,
                )
            except (asyncio.TimeoutError, asyncio.CancelledError):
                pass

    def _start_poll_task(self, rule: RuleState) -> None:
        """Start an async polling task for the given rule."""
        self._cancel_poll_task(rule.rule_id)
        if self._loop and self._loop.is_running():
            task = self._loop.create_task(
                self._poll_task(rule.rule_id),
                name=f"poll-{rule.rule_ref}",
            )
            self._poll_tasks[rule.rule_id] = task

    def _cancel_poll_task(self, rule_id: int) -> None:
        """Cancel the polling task for a rule."""
        task = self._poll_tasks.pop(rule_id, None)
        if task and not task.done():
            task.cancel()

    # Rule lifecycle hooks

    def on_rule_created(self, rule: RuleState) -> None:
        self._start_poll_task(rule)

    def on_rule_enabled(self, rule: RuleState) -> None:
        self._start_poll_task(rule)

    def on_rule_disabled(self, rule: RuleState) -> None:
        self._cancel_poll_task(rule.rule_id)

    def on_rule_deleted(self, rule: RuleState) -> None:
        self._cancel_poll_task(rule.rule_id)

    def on_rule_updated(self, rule: RuleState, old_params: dict[str, Any]) -> None:
        self._start_poll_task(rule)

    async def _async_run(self) -> None:
        """Main async entry point."""
        self._loop = asyncio.get_event_loop()
        try:
            await self.setup()

            # Start poll tasks for any rules bootstrapped before the loop started
            with self._rules_lock:
                for rule in self._rules.values():
                    if rule.enabled:
                        self._start_poll_task(rule)

            # Wait for shutdown
            while not self._shutdown_event.is_set():
                await asyncio.sleep(1)
        finally:
            # Cancel all poll tasks
            for rule_id in list(self._poll_tasks.keys()):
                self._cancel_poll_task(rule_id)
            # Let cancelled tasks finish
            pending = [t for t in self._poll_tasks.values() if not t.done()]
            if pending:
                await asyncio.gather(*pending, return_exceptions=True)
            await self.cleanup()
            if self._async_http_client is not None:
                await self._async_http_client.aclose()
                self._async_http_client = None

    def run(self) -> None:
        """Run the async event loop."""
        asyncio.run(self._async_run())

    def _run_lifecycle(self) -> int:
        """Override to skip calling sync setup/cleanup (handled in _async_run)."""
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        mq_thread = None
        try:
            self._bootstrap_rules()
            mq_thread = self._start_mq_consumer()
            self.logger.info("Sensor started", extra={"active_rules": len(self._rules)})
            self.run()
        except Exception as exc:
            self.logger.error("Sensor error: %s", exc)
            return 1
        finally:
            self._shutdown_event.set()
            if self._http_client is not None:
                self._http_client.close()
                self._http_client = None
            if mq_thread:
                mq_thread.join(timeout=5)
            self.logger.info("Sensor stopped")

        return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def run_sensor(sensor_class: type[Sensor]) -> None:
    """Instantiate and run a sensor class.

    Args:
        sensor_class: A subclass of :class:`Sensor`, :class:`PollingSensor`,
            or :class:`AsyncPollingSensor`.
    """
    sensor = sensor_class()
    code = sensor._run_lifecycle()
    sys.exit(code)

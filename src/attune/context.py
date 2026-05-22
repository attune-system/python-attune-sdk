"""
Execution context — module-level singletons providing access to environment
variables and execution metadata.

These are computed once at import time from environment variables and are
immutable for the lifetime of the process (which is a single action execution
or sensor run).

Usage::

    from attune.context import action_context
    # or
    import attune
    print(attune.context.execution_id)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from attune.api_client import AuthenticatedClient


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
        mq_url: The RabbitMQ connection URL.
        mq_exchange: The RabbitMQ exchange name.
        log_level: The configured log level.
        pack_ref: The pack reference derived from sensor_ref.
    """

    sensor_ref: str
    sensor_id: str
    api_url: str
    api_token: str
    mq_url: str
    mq_exchange: str
    log_level: str
    pack_ref: str

    @property
    def config(self) -> dict[str, str]:
        """Sensor-specific config from ATTUNE_SENSOR_CONFIG_* environment variables."""
        prefix = "ATTUNE_SENSOR_CONFIG_"
        return {
            k[len(prefix):].lower(): v
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
    sensor_ref = os.environ.get("ATTUNE_SENSOR_REF", "")
    parts = sensor_ref.split(".")
    pack_ref = parts[0] if len(parts) >= 2 else ""
    return SensorContext(
        sensor_ref=sensor_ref,
        sensor_id=os.environ.get("ATTUNE_SENSOR_ID", "0"),
        api_url=os.environ.get("ATTUNE_API_URL", "http://localhost:8080"),
        api_token=os.environ.get("ATTUNE_API_TOKEN", ""),
        mq_url=os.environ.get("ATTUNE_MQ_URL", "amqp://localhost:5672"),
        mq_exchange=os.environ.get("ATTUNE_MQ_EXCHANGE", "attune"),
        log_level=os.environ.get("ATTUNE_LOG_LEVEL", "info").upper(),
        pack_ref=pack_ref,
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
    if _sensor_client is None:
        from attune.api_client import AuthenticatedClient

        _sensor_client = AuthenticatedClient(
            base_url=ctx.api_url,
            token=ctx.api_token,
        )
    return _sensor_client


#: Module-level action context singleton. Computed once at import time.
action_context: ActionContext = _build_action_context()

#: Module-level sensor context singleton. Computed once at import time.
sensor_context: SensorContext = _build_sensor_context()

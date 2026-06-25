"""
Attune Python SDK — helpers for building actions and sensors.

Quick start for actions::

    import attune

    def main(name: str, count: int = 1):
        return {"greeting": f"Hello, {name}!" * count}

    attune.run_action(main)

Quick start for sensors::

    import attune

    class MySensor(attune.PollingSensor):
        def setup(self):
            self.interval = 5.0

        def poll(self, rule):
            self.emit({"value": 42}, rule=rule)

    attune.run_sensor(MySensor)

Access execution context anywhere::

    import attune
    print(attune.context.execution_id)      # action context
    print(attune.sensor_context.sensor_ref)  # sensor context
"""

from . import artifacts
from .action import run_action
from .api_client import AuthenticatedClient, Client
from .artifacts import ArtifactAllocation, ProgressArtifact, allocate_file_version, create_progress
from .client import AttuneClient
from .context import (
    ActionContext,
    SensorContext,
    action_context as context,
    sensor_context,
)
from .sensor import AsyncPollingSensor, PollingSensor, RuleState, Sensor, run_sensor

__all__ = [
    "artifacts",
    "ArtifactAllocation",
    "ProgressArtifact",
    "allocate_file_version",
    "create_progress",
    "run_action",
    "run_sensor",
    "context",
    "sensor_context",
    "ActionContext",
    "AsyncPollingSensor",
    "AttuneClient",
    "AuthenticatedClient",
    "Client",
    "PollingSensor",
    "RuleState",
    "Sensor",
    "SensorContext",
]

__version__ = "0.1.0"

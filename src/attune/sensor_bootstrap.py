"""Bounded, one-shot stdin delivery for managed sensor values."""

import json
import sys
from dataclasses import dataclass
from typing import Any, BinaryIO

MAX_BOOTSTRAP_BYTES = 32 * 1024 * 1024


@dataclass(frozen=True, repr=False)
class SensorBootstrap:
    config: dict[str, Any]
    triggers: list[dict[str, Any]]


def read_sensor_bootstrap(reader: BinaryIO) -> SensorBootstrap:
    try:
        raw = reader.read(MAX_BOOTSTRAP_BYTES + 1)
    except OSError:
        raise ValueError("Cannot read sensor bootstrap") from None
    if len(raw) > MAX_BOOTSTRAP_BYTES:
        raise ValueError("Sensor bootstrap exceeds its delivery limit")
    if not raw:
        raise ValueError(
            "Missing sensor stdin bootstrap: provide a JSON object with config "
            "and triggers, then close stdin. Environment-based sensor startup "
            "is not supported by this SDK."
        )
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError):
        raise ValueError("Invalid sensor bootstrap JSON") from None
    if (
        not isinstance(value, dict)
        or set(value) != {"config", "triggers"}
        or not isinstance(value["config"], dict)
        or not isinstance(value["triggers"], list)
        or any(not isinstance(item, dict) for item in value["triggers"])
    ):
        raise ValueError("Invalid sensor bootstrap sections")
    return SensorBootstrap(config=value["config"], triggers=value["triggers"])


class SensorBootstrapState:
    """Read only when a sensor needs its values, never during action imports."""

    def __init__(self, reader: BinaryIO | None = None) -> None:
        self._reader = reader
        self._value: SensorBootstrap | None = None

    def get(self) -> SensorBootstrap:
        if self._value is None:
            self._value = read_sensor_bootstrap(self._reader or sys.stdin.buffer)
        return self._value

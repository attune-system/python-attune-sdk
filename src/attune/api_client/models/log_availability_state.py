from enum import Enum


class LogAvailabilityState(str, Enum):
    EMPTY = "empty"
    FINALIZING = "finalizing"
    INCOMPLETE = "incomplete"
    READY = "ready"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)

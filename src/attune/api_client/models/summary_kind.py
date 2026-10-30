from enum import Enum


class SummaryKind(str, Enum):
    EVENT_VOLUME = "event_volume"
    EXECUTION_CREATION = "execution_creation"
    EXECUTION_STATUS = "execution_status"
    WORKER_STATUS = "worker_status"

    def __str__(self) -> str:
        return str(self.value)

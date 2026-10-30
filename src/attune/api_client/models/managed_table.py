from enum import Enum


class ManagedTable(str, Enum):
    AUDIT_EVENT = "audit_event"
    EVENT = "event"
    EXECUTION_HISTORY = "execution_history"

    def __str__(self) -> str:
        return str(self.value)

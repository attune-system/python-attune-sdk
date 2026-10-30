from enum import Enum


class TriggerClearOperation(str, Enum):
    CLEAR = "clear"

    def __str__(self) -> str:
        return str(self.value)

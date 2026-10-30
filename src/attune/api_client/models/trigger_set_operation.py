from enum import Enum


class TriggerSetOperation(str, Enum):
    SET = "set"

    def __str__(self) -> str:
        return str(self.value)

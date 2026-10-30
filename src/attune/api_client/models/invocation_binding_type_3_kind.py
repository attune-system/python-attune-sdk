from enum import Enum


class InvocationBindingType3Kind(str, Enum):
    QUEUE = "queue"

    def __str__(self) -> str:
        return str(self.value)

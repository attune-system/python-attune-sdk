from enum import Enum


class InvocationBindingType2Kind(str, Enum):
    RULE = "rule"

    def __str__(self) -> str:
        return str(self.value)

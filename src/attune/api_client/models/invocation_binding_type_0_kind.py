from enum import Enum


class InvocationBindingType0Kind(str, Enum):
    ACTION = "action"

    def __str__(self) -> str:
        return str(self.value)

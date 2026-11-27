from enum import Enum


class OptionStyle(str, Enum):
    ATTACHED = "attached"
    EQUALS = "equals"
    SEPARATE = "separate"

    def __str__(self) -> str:
        return str(self.value)

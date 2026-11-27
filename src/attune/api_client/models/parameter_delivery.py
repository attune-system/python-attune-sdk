from enum import Enum


class ParameterDelivery(str, Enum):
    FILE = "file"
    NONE = "none"
    STDIN = "stdin"

    def __str__(self) -> str:
        return str(self.value)

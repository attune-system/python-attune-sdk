from enum import Enum


class CliBindingType0Kind(str, Enum):
    POSITIONAL = "positional"

    def __str__(self) -> str:
        return str(self.value)

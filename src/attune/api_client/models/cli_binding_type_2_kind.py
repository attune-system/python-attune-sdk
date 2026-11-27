from enum import Enum


class CliBindingType2Kind(str, Enum):
    FLAG = "flag"

    def __str__(self) -> str:
        return str(self.value)

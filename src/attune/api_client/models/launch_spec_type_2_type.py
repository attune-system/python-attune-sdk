from enum import Enum


class LaunchSpecType2Type(str, Enum):
    NATIVE = "native"

    def __str__(self) -> str:
        return str(self.value)

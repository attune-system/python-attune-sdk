from enum import Enum


class LaunchSpecType0Type(str, Enum):
    COMMAND = "command"

    def __str__(self) -> str:
        return str(self.value)

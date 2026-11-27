from enum import Enum


class LaunchSpecType1Type(str, Enum):
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)

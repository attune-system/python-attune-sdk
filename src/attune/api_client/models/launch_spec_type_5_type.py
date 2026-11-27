from enum import Enum


class LaunchSpecType5Type(str, Enum):
    INTRINSIC = "intrinsic"

    def __str__(self) -> str:
        return str(self.value)

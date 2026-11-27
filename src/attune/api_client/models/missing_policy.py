from enum import Enum


class MissingPolicy(str, Enum):
    ERROR = "error"
    OMIT = "omit"

    def __str__(self) -> str:
        return str(self.value)

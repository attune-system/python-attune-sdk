from enum import Enum


class Encoding(str, Enum):
    JSON = "json"
    SCALAR = "scalar"

    def __str__(self) -> str:
        return str(self.value)

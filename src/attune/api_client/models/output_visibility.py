from enum import Enum


class OutputVisibility(str, Enum):
    PUBLIC = "public"
    SECRET = "secret"

    def __str__(self) -> str:
        return str(self.value)

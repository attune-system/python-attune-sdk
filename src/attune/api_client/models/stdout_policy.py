from enum import Enum


class StdoutPolicy(str, Enum):
    PUBLIC = "public"
    SANITIZED = "sanitized"
    SECRET = "secret"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class OidcDevicePollResponse200DataType0Status(str, Enum):
    WAITING = "waiting"

    def __str__(self) -> str:
        return str(self.value)

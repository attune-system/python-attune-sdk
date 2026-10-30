from enum import Enum


class OidcDevicePollResponse200DataType3Status(str, Enum):
    EXPIRED = "expired"

    def __str__(self) -> str:
        return str(self.value)

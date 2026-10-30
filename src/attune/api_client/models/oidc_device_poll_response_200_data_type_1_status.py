from enum import Enum


class OidcDevicePollResponse200DataType1Status(str, Enum):
    AUTHORIZED = "authorized"

    def __str__(self) -> str:
        return str(self.value)

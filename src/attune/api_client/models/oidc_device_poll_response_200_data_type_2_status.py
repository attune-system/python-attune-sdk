from enum import Enum


class OidcDevicePollResponse200DataType2Status(str, Enum):
    ACCESS_DENIED = "access_denied"

    def __str__(self) -> str:
        return str(self.value)

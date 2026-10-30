from enum import Enum


class DeviceWaitReason(str, Enum):
    AUTHORIZATION_PENDING = "authorization_pending"
    PROVIDER_TIMEOUT = "provider_timeout"
    SLOW_DOWN = "slow_down"

    def __str__(self) -> str:
        return str(self.value)

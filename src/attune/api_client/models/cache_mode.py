from enum import Enum


class CacheMode(str, Enum):
    LIVE = "live"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)

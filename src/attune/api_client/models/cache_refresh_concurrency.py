from enum import Enum


class CacheRefreshConcurrency(str, Enum):
    CONFLICT = "conflict"
    PARALLEL = "parallel"
    REUSE = "reuse"

    def __str__(self) -> str:
        return str(self.value)

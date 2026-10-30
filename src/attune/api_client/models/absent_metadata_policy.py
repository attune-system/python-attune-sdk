from enum import Enum


class AbsentMetadataPolicy(str, Enum):
    DISABLE = "disable"
    REMOVE = "remove"
    RETAIN = "retain"

    def __str__(self) -> str:
        return str(self.value)

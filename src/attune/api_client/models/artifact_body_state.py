from enum import Enum


class ArtifactBodyState(str, Enum):
    DELETING = "deleting"
    PENDING = "pending"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)

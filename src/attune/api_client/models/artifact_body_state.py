from enum import Enum


class ArtifactBodyState(str, Enum):
    CLEANUP_CLAIMED = "cleanup_claimed"
    DELETING = "deleting"
    PENDING = "pending"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)

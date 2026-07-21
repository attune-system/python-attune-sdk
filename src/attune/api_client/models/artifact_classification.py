from enum import Enum


class ArtifactClassification(str, Enum):
    GENERAL = "general"
    RUNTIME_LOG = "runtime_log"

    def __str__(self) -> str:
        return str(self.value)

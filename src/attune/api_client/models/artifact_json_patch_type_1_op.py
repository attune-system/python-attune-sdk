from enum import Enum


class ArtifactJsonPatchType1Op(str, Enum):
    CLEAR = "clear"

    def __str__(self) -> str:
        return str(self.value)

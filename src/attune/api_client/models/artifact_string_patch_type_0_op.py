from enum import Enum


class ArtifactStringPatchType0Op(str, Enum):
    SET = "set"

    def __str__(self) -> str:
        return str(self.value)

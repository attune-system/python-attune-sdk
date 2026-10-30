from enum import Enum


class ExecutionOptionsAuthoritySource(str, Enum):
    HUMAN_DELEGATION = "human_delegation"
    PACK = "pack"

    def __str__(self) -> str:
        return str(self.value)

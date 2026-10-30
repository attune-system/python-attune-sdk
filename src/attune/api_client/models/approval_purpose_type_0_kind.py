from enum import Enum


class ApprovalPurposeType0Kind(str, Enum):
    RUNTIME = "runtime"

    def __str__(self) -> str:
        return str(self.value)

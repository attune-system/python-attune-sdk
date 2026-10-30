from enum import Enum


class ApprovalPurposeType1Kind(str, Enum):
    DECLARED_INPUT = "declared_input"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class IntrinsicHandler(str, Enum):
    ATTUNE_INQUIRYV1 = "attune.inquiry/v1"

    def __str__(self) -> str:
        return str(self.value)

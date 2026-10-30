from enum import Enum


class InquiryResponseOptionStyle(str, Enum):
    DEFAULT = "default"
    DESTRUCTIVE = "destructive"
    POSITIVE = "positive"

    def __str__(self) -> str:
        return str(self.value)

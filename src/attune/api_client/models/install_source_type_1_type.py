from enum import Enum


class InstallSourceType1Type(str, Enum):
    ARCHIVE = "archive"

    def __str__(self) -> str:
        return str(self.value)

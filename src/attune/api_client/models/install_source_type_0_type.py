from enum import Enum


class InstallSourceType0Type(str, Enum):
    GIT = "git"

    def __str__(self) -> str:
        return str(self.value)

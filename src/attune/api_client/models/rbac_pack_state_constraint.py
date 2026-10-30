from enum import Enum


class RbacPackStateConstraint(str, Enum):
    UNINSTALLED = "uninstalled"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class RbacPackOwnerConstraint(str, Enum):
    SELF = "self"

    def __str__(self) -> str:
        return str(self.value)

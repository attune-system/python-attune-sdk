from enum import Enum


class RbacOwnerConstraint(str, Enum):
    ANY = "any"
    NONE = "none"
    SELF = "self"

    def __str__(self) -> str:
        return str(self.value)

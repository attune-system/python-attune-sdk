from enum import Enum


class RbacExecutionScopeConstraint(str, Enum):
    ANY = "any"
    DESCENDANTS = "descendants"
    SELF = "self"

    def __str__(self) -> str:
        return str(self.value)

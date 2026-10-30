from enum import Enum


class PermissionRoleTargetType(str, Enum):
    ROLE = "role"

    def __str__(self) -> str:
        return str(self.value)

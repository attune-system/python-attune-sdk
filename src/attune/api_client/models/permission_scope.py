from enum import Enum


class PermissionScope(str, Enum):
    EXTERNAL = "external"
    PACK = "pack"

    def __str__(self) -> str:
        return str(self.value)

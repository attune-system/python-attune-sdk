from enum import Enum


class PlatformCatalogStatus(str, Enum):
    CURRENT = "current"
    INCOMPATIBLE = "incompatible"
    UPGRADE_REQUIRED = "upgrade_required"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class PackDiagnosticSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)

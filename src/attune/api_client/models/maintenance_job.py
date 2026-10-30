from enum import Enum


class MaintenanceJob(str, Enum):
    PARTITION = "partition"
    RETENTION = "retention"
    SUMMARY = "summary"

    def __str__(self) -> str:
        return str(self.value)

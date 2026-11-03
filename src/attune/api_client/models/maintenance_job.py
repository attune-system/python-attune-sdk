from enum import Enum


class MaintenanceJob(str, Enum):
    OBJECT_RETENTION = "object_retention"
    PARTITION = "partition"
    RETENTION = "retention"
    SUMMARY = "summary"

    def __str__(self) -> str:
        return str(self.value)

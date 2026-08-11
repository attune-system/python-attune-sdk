from enum import Enum


class WorkflowCacheIterationState(str, Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    SCANNING = "scanning"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class WorkflowTaskWaitState(str, Enum):
    CANCELLED = "cancelled"
    FAILED = "failed"
    RELEASED = "released"
    TIMED_OUT = "timed_out"
    WAITING = "waiting"

    def __str__(self) -> str:
        return str(self.value)

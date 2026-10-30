from enum import Enum


class InvocationBindingType1Kind(str, Enum):
    WORKFLOW_TASK = "workflow_task"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class LaunchSpecType4Type(str, Enum):
    JAVA_CLASS = "java_class"

    def __str__(self) -> str:
        return str(self.value)

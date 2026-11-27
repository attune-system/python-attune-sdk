from enum import Enum


class LaunchSpecType3Type(str, Enum):
    JAVA_JAR = "java_jar"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class CliBindingType1Kind(str, Enum):
    OPTION = "option"

    def __str__(self) -> str:
        return str(self.value)

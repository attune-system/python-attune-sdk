from enum import Enum


class ParameterFormat(str, Enum):
    DOTENV = "dotenv"
    JSON = "json"
    YAML = "yaml"

    def __str__(self) -> str:
        return str(self.value)

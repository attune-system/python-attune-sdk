from enum import Enum


class OutputFormat(str, Enum):
    JSON = "json"
    JSONL = "jsonl"
    TEXT = "text"
    YAML = "yaml"

    def __str__(self) -> str:
        return str(self.value)

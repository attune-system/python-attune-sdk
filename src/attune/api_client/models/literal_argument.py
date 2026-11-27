from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="LiteralArgument")


@_attrs_define
class LiteralArgument:
    """One immutable token, ordered together with the parameter bindings.

    Attributes:
        literal (str):
        order (int):
    """

    literal: str
    order: int

    def to_dict(self) -> dict[str, Any]:
        literal = self.literal

        order = self.order

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "literal": literal,
                "order": order,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        literal = d.pop("literal")

        order = d.pop("order")

        literal_argument = cls(
            literal=literal,
            order=order,
        )

        return literal_argument

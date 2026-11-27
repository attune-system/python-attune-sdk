from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.cli_binding_type_0_kind import CliBindingType0Kind
from ..models.encoding import Encoding
from ..types import UNSET, Unset

T = TypeVar("T", bound="CliBindingType0")


@_attrs_define
class CliBindingType0:
    """
    Attributes:
        kind (CliBindingType0Kind):
        order (int):
        encoding (Encoding | Unset):
        expand (bool | Unset):
    """

    kind: CliBindingType0Kind
    order: int
    encoding: Encoding | Unset = UNSET
    expand: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        order = self.order

        encoding: str | Unset = UNSET
        if not isinstance(self.encoding, Unset):
            encoding = self.encoding.value

        expand = self.expand

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "order": order,
            }
        )
        if encoding is not UNSET:
            field_dict["encoding"] = encoding
        if expand is not UNSET:
            field_dict["expand"] = expand

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        kind = CliBindingType0Kind(d.pop("kind"))

        order = d.pop("order")

        _encoding = d.pop("encoding", UNSET)
        encoding: Encoding | Unset
        if isinstance(_encoding, Unset):
            encoding = UNSET
        else:
            encoding = Encoding(_encoding)

        expand = d.pop("expand", UNSET)

        cli_binding_type_0 = cls(
            kind=kind,
            order=order,
            encoding=encoding,
            expand=expand,
        )

        cli_binding_type_0.additional_properties = d
        return cli_binding_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.cli_binding_type_1_kind import CliBindingType1Kind
from ..models.encoding import Encoding
from ..models.missing_policy import MissingPolicy
from ..models.option_style import OptionStyle
from ..types import UNSET, Unset

T = TypeVar("T", bound="CliBindingType1")


@_attrs_define
class CliBindingType1:
    """
    Attributes:
        kind (CliBindingType1Kind):
        name (str):
        order (int):
        encoding (Encoding | Unset):
        expand (bool | Unset):
        missing (MissingPolicy | Unset):
        style (OptionStyle | Unset):
    """

    kind: CliBindingType1Kind
    name: str
    order: int
    encoding: Encoding | Unset = UNSET
    expand: bool | Unset = UNSET
    missing: MissingPolicy | Unset = UNSET
    style: OptionStyle | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        name = self.name

        order = self.order

        encoding: str | Unset = UNSET
        if not isinstance(self.encoding, Unset):
            encoding = self.encoding.value

        expand = self.expand

        missing: str | Unset = UNSET
        if not isinstance(self.missing, Unset):
            missing = self.missing.value

        style: str | Unset = UNSET
        if not isinstance(self.style, Unset):
            style = self.style.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "name": name,
                "order": order,
            }
        )
        if encoding is not UNSET:
            field_dict["encoding"] = encoding
        if expand is not UNSET:
            field_dict["expand"] = expand
        if missing is not UNSET:
            field_dict["missing"] = missing
        if style is not UNSET:
            field_dict["style"] = style

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        kind = CliBindingType1Kind(d.pop("kind"))

        name = d.pop("name")

        order = d.pop("order")

        _encoding = d.pop("encoding", UNSET)
        encoding: Encoding | Unset
        if isinstance(_encoding, Unset):
            encoding = UNSET
        else:
            encoding = Encoding(_encoding)

        expand = d.pop("expand", UNSET)

        _missing = d.pop("missing", UNSET)
        missing: MissingPolicy | Unset
        if isinstance(_missing, Unset):
            missing = UNSET
        else:
            missing = MissingPolicy(_missing)

        _style = d.pop("style", UNSET)
        style: OptionStyle | Unset
        if isinstance(_style, Unset):
            style = UNSET
        else:
            style = OptionStyle(_style)

        cli_binding_type_1 = cls(
            kind=kind,
            name=name,
            order=order,
            encoding=encoding,
            expand=expand,
            missing=missing,
            style=style,
        )

        cli_binding_type_1.additional_properties = d
        return cli_binding_type_1

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

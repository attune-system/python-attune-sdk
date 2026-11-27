from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.cli_binding_type_2_kind import CliBindingType2Kind
from ..models.missing_policy import MissingPolicy
from ..types import UNSET, Unset

T = TypeVar("T", bound="CliBindingType2")


@_attrs_define
class CliBindingType2:
    """
    Attributes:
        kind (CliBindingType2Kind):
        name (str):
        order (int):
        false_name (None | str | Unset):
        missing (MissingPolicy | Unset):
    """

    kind: CliBindingType2Kind
    name: str
    order: int
    false_name: None | str | Unset = UNSET
    missing: MissingPolicy | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        name = self.name

        order = self.order

        false_name: None | str | Unset
        if isinstance(self.false_name, Unset):
            false_name = UNSET
        else:
            false_name = self.false_name

        missing: str | Unset = UNSET
        if not isinstance(self.missing, Unset):
            missing = self.missing.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "name": name,
                "order": order,
            }
        )
        if false_name is not UNSET:
            field_dict["false_name"] = false_name
        if missing is not UNSET:
            field_dict["missing"] = missing

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        kind = CliBindingType2Kind(d.pop("kind"))

        name = d.pop("name")

        order = d.pop("order")

        def _parse_false_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        false_name = _parse_false_name(d.pop("false_name", UNSET))

        _missing = d.pop("missing", UNSET)
        missing: MissingPolicy | Unset
        if isinstance(_missing, Unset):
            missing = UNSET
        else:
            missing = MissingPolicy(_missing)

        cli_binding_type_2 = cls(
            kind=kind,
            name=name,
            order=order,
            false_name=false_name,
            missing=missing,
        )

        cli_binding_type_2.additional_properties = d
        return cli_binding_type_2

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

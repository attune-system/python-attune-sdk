from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="PackOwnershipMetadata")


@_attrs_define
class PackOwnershipMetadata:
    """
    Attributes:
        owner_roles (list[str] | Unset):
    """

    owner_roles: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_roles: list[str] | Unset = UNSET
        if not isinstance(self.owner_roles, Unset):
            owner_roles = self.owner_roles

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if owner_roles is not UNSET:
            field_dict["owner_roles"] = owner_roles

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        owner_roles = cast(list[str], d.pop("owner_roles", UNSET))

        pack_ownership_metadata = cls(
            owner_roles=owner_roles,
        )

        pack_ownership_metadata.additional_properties = d
        return pack_ownership_metadata

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

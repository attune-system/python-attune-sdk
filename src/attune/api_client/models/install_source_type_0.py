from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.install_source_type_0_type import InstallSourceType0Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="InstallSourceType0")


@_attrs_define
class InstallSourceType0:
    """Git repository source

    Attributes:
        checksum (str): Checksum in format "algorithm:hash"
        type_ (InstallSourceType0Type):
        url (str): Git repository URL
        ref (None | str | Unset): Git ref (tag, branch, commit)
    """

    checksum: str
    type_: InstallSourceType0Type
    url: str
    ref: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checksum = self.checksum

        type_ = self.type_.value

        url = self.url

        ref: None | str | Unset
        if isinstance(self.ref, Unset):
            ref = UNSET
        else:
            ref = self.ref

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checksum": checksum,
                "type": type_,
                "url": url,
            }
        )
        if ref is not UNSET:
            field_dict["ref"] = ref

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        checksum = d.pop("checksum")

        type_ = InstallSourceType0Type(d.pop("type"))

        url = d.pop("url")

        def _parse_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ref = _parse_ref(d.pop("ref", UNSET))

        install_source_type_0 = cls(
            checksum=checksum,
            type_=type_,
            url=url,
            ref=ref,
        )

        install_source_type_0.additional_properties = d
        return install_source_type_0

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

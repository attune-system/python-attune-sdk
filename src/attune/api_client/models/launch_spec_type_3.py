from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.launch_spec_type_3_type import LaunchSpecType3Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="LaunchSpecType3")


@_attrs_define
class LaunchSpecType3:
    """
    Attributes:
        artifact (str):
        type_ (LaunchSpecType3Type):
        jvm_args (list[str] | Unset):
    """

    artifact: str
    type_: LaunchSpecType3Type
    jvm_args: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        artifact = self.artifact

        type_ = self.type_.value

        jvm_args: list[str] | Unset = UNSET
        if not isinstance(self.jvm_args, Unset):
            jvm_args = self.jvm_args

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "artifact": artifact,
                "type": type_,
            }
        )
        if jvm_args is not UNSET:
            field_dict["jvm_args"] = jvm_args

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        artifact = d.pop("artifact")

        type_ = LaunchSpecType3Type(d.pop("type"))

        jvm_args = cast(list[str], d.pop("jvm_args", UNSET))

        launch_spec_type_3 = cls(
            artifact=artifact,
            type_=type_,
            jvm_args=jvm_args,
        )

        launch_spec_type_3.additional_properties = d
        return launch_spec_type_3

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

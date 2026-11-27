from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.launch_spec_type_2_type import LaunchSpecType2Type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.literal_argument import LiteralArgument


T = TypeVar("T", bound="LaunchSpecType2")


@_attrs_define
class LaunchSpecType2:
    """
    Attributes:
        artifact (str):
        type_ (LaunchSpecType2Type):
        arguments (list[LiteralArgument] | Unset):
    """

    artifact: str
    type_: LaunchSpecType2Type
    arguments: list[LiteralArgument] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        artifact = self.artifact

        type_ = self.type_.value

        arguments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = []
            for arguments_item_data in self.arguments:
                arguments_item = arguments_item_data.to_dict()
                arguments.append(arguments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "artifact": artifact,
                "type": type_,
            }
        )
        if arguments is not UNSET:
            field_dict["arguments"] = arguments

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.literal_argument import LiteralArgument

        d = dict(src_dict)
        artifact = d.pop("artifact")

        type_ = LaunchSpecType2Type(d.pop("type"))

        _arguments = d.pop("arguments", UNSET)
        arguments: list[LiteralArgument] | Unset = UNSET
        if _arguments is not UNSET:
            arguments = []
            for arguments_item_data in _arguments:
                arguments_item = LiteralArgument.from_dict(arguments_item_data)

                arguments.append(arguments_item)

        launch_spec_type_2 = cls(
            artifact=artifact,
            type_=type_,
            arguments=arguments,
        )

        launch_spec_type_2.additional_properties = d
        return launch_spec_type_2

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

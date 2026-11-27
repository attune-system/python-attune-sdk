from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.intrinsic_handler import IntrinsicHandler
from ..models.launch_spec_type_5_type import LaunchSpecType5Type

T = TypeVar("T", bound="LaunchSpecType5")


@_attrs_define
class LaunchSpecType5:
    """
    Attributes:
        handler (IntrinsicHandler):
        type_ (LaunchSpecType5Type):
    """

    handler: IntrinsicHandler
    type_: LaunchSpecType5Type
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        handler = self.handler.value

        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "handler": handler,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        handler = IntrinsicHandler(d.pop("handler"))

        type_ = LaunchSpecType5Type(d.pop("type"))

        launch_spec_type_5 = cls(
            handler=handler,
            type_=type_,
        )

        launch_spec_type_5.additional_properties = d
        return launch_spec_type_5

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

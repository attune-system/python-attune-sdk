from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.invocation_binding_type_0_kind import InvocationBindingType0Kind

T = TypeVar("T", bound="InvocationBindingType0")


@_attrs_define
class InvocationBindingType0:
    """
    Attributes:
        action_ref (str):
        kind (InvocationBindingType0Kind):
    """

    action_ref: str
    kind: InvocationBindingType0Kind
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_ref = self.action_ref

        kind = self.kind.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action_ref": action_ref,
                "kind": kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        action_ref = d.pop("action_ref")

        kind = InvocationBindingType0Kind(d.pop("kind"))

        invocation_binding_type_0 = cls(
            action_ref=action_ref,
            kind=kind,
        )

        invocation_binding_type_0.additional_properties = d
        return invocation_binding_type_0

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.invocation_binding_type_2_kind import InvocationBindingType2Kind

T = TypeVar("T", bound="InvocationBindingType2")


@_attrs_define
class InvocationBindingType2:
    """
    Attributes:
        action_ref (str):
        kind (InvocationBindingType2Kind):
        rule_ref (str):
    """

    action_ref: str
    kind: InvocationBindingType2Kind
    rule_ref: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_ref = self.action_ref

        kind = self.kind.value

        rule_ref = self.rule_ref

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action_ref": action_ref,
                "kind": kind,
                "rule_ref": rule_ref,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        action_ref = d.pop("action_ref")

        kind = InvocationBindingType2Kind(d.pop("kind"))

        rule_ref = d.pop("rule_ref")

        invocation_binding_type_2 = cls(
            action_ref=action_ref,
            kind=kind,
            rule_ref=rule_ref,
        )

        invocation_binding_type_2.additional_properties = d
        return invocation_binding_type_2

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

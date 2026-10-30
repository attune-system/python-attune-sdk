from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.invocation_binding_type_1_kind import InvocationBindingType1Kind

T = TypeVar("T", bound="InvocationBindingType1")


@_attrs_define
class InvocationBindingType1:
    """
    Attributes:
        action_ref (str):
        kind (InvocationBindingType1Kind):
        task_path (str):
        workflow_ref (str):
    """

    action_ref: str
    kind: InvocationBindingType1Kind
    task_path: str
    workflow_ref: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_ref = self.action_ref

        kind = self.kind.value

        task_path = self.task_path

        workflow_ref = self.workflow_ref

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action_ref": action_ref,
                "kind": kind,
                "task_path": task_path,
                "workflow_ref": workflow_ref,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        action_ref = d.pop("action_ref")

        kind = InvocationBindingType1Kind(d.pop("kind"))

        task_path = d.pop("task_path")

        workflow_ref = d.pop("workflow_ref")

        invocation_binding_type_1 = cls(
            action_ref=action_ref,
            kind=kind,
            task_path=task_path,
            workflow_ref=workflow_ref,
        )

        invocation_binding_type_1.additional_properties = d
        return invocation_binding_type_1

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

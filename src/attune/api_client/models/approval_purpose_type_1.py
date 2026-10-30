from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.approval_purpose_type_1_kind import ApprovalPurposeType1Kind

if TYPE_CHECKING:
    from ..models.declared_input_approval_target import DeclaredInputApprovalTarget


T = TypeVar("T", bound="ApprovalPurposeType1")


@_attrs_define
class ApprovalPurposeType1:
    """
    Attributes:
        kind (ApprovalPurposeType1Kind):
        targets (list[DeclaredInputApprovalTarget]): Only currently visible retained targets. Empty when target rows
            were
            collected or current component visibility denies disclosure. Purpose
            never falls back to runtime merely because no target is visible.
    """

    kind: ApprovalPurposeType1Kind
    targets: list[DeclaredInputApprovalTarget]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        targets = []
        for targets_item_data in self.targets:
            targets_item = targets_item_data.to_dict()
            targets.append(targets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "targets": targets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.declared_input_approval_target import DeclaredInputApprovalTarget

        d = dict(src_dict)
        kind = ApprovalPurposeType1Kind(d.pop("kind"))

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:
            targets_item = DeclaredInputApprovalTarget.from_dict(targets_item_data)

            targets.append(targets_item)

        approval_purpose_type_1 = cls(
            kind=kind,
            targets=targets,
        )

        approval_purpose_type_1.additional_properties = d
        return approval_purpose_type_1

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

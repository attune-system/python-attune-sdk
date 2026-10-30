from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.execution_options_authority_source import ExecutionOptionsAuthoritySource
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetExecutionOptionsResponse200Data")


@_attrs_define
class GetExecutionOptionsResponse200Data:
    """
    Attributes:
        action_ref (str):
        authority_source (ExecutionOptionsAuthoritySource):
        default_permission_set_refs (list[str]):
        default_selection_available (bool): Informational only. Actual creation rechecks admission and revocation.
        selectable_permission_set_refs (list[str]):
        policy_revision_id (int | None | Unset):
    """

    action_ref: str
    authority_source: ExecutionOptionsAuthoritySource
    default_permission_set_refs: list[str]
    default_selection_available: bool
    selectable_permission_set_refs: list[str]
    policy_revision_id: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_ref = self.action_ref

        authority_source = self.authority_source.value

        default_permission_set_refs = self.default_permission_set_refs

        default_selection_available = self.default_selection_available

        selectable_permission_set_refs = self.selectable_permission_set_refs

        policy_revision_id: int | None | Unset
        if isinstance(self.policy_revision_id, Unset):
            policy_revision_id = UNSET
        else:
            policy_revision_id = self.policy_revision_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action_ref": action_ref,
                "authority_source": authority_source,
                "default_permission_set_refs": default_permission_set_refs,
                "default_selection_available": default_selection_available,
                "selectable_permission_set_refs": selectable_permission_set_refs,
            }
        )
        if policy_revision_id is not UNSET:
            field_dict["policy_revision_id"] = policy_revision_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        action_ref = d.pop("action_ref")

        authority_source = ExecutionOptionsAuthoritySource(d.pop("authority_source"))

        default_permission_set_refs = cast(
            list[str], d.pop("default_permission_set_refs")
        )

        default_selection_available = d.pop("default_selection_available")

        selectable_permission_set_refs = cast(
            list[str], d.pop("selectable_permission_set_refs")
        )

        def _parse_policy_revision_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        policy_revision_id = _parse_policy_revision_id(
            d.pop("policy_revision_id", UNSET)
        )

        get_execution_options_response_200_data = cls(
            action_ref=action_ref,
            authority_source=authority_source,
            default_permission_set_refs=default_permission_set_refs,
            default_selection_available=default_selection_available,
            selectable_permission_set_refs=selectable_permission_set_refs,
            policy_revision_id=policy_revision_id,
        )

        get_execution_options_response_200_data.additional_properties = d
        return get_execution_options_response_200_data

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="ResourceParticipant")


@_attrs_define
class ResourceParticipant:
    """
    Attributes:
        action (str):
        resource_parameter (str):
    """

    action: str
    resource_parameter: str

    def to_dict(self) -> dict[str, Any]:
        action = self.action

        resource_parameter = self.resource_parameter

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "action": action,
                "resource_parameter": resource_parameter,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        action = d.pop("action")

        resource_parameter = d.pop("resource_parameter")

        resource_participant = cls(
            action=action,
            resource_parameter=resource_parameter,
        )

        return resource_participant

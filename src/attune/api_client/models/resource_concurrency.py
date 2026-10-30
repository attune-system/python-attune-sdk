from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.policy_method import PolicyMethod

if TYPE_CHECKING:
    from ..models.resource_participant import ResourceParticipant


T = TypeVar("T", bound="ResourceConcurrency")


@_attrs_define
class ResourceConcurrency:
    """
    Attributes:
        limit (int):
        method (PolicyMethod):
        namespace (str):
        participants (list[ResourceParticipant]):
    """

    limit: int
    method: PolicyMethod
    namespace: str
    participants: list[ResourceParticipant]

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        method = self.method.value

        namespace = self.namespace

        participants = []
        for participants_item_data in self.participants:
            participants_item = participants_item_data.to_dict()
            participants.append(participants_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "limit": limit,
                "method": method,
                "namespace": namespace,
                "participants": participants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.resource_participant import ResourceParticipant

        d = dict(src_dict)
        limit = d.pop("limit")

        method = PolicyMethod(d.pop("method"))

        namespace = d.pop("namespace")

        participants = []
        _participants = d.pop("participants")
        for participants_item_data in _participants:
            participants_item = ResourceParticipant.from_dict(participants_item_data)

            participants.append(participants_item)

        resource_concurrency = cls(
            limit=limit,
            method=method,
            namespace=namespace,
            participants=participants,
        )

        return resource_concurrency

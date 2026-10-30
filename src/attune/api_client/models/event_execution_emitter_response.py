from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="EventExecutionEmitterResponse")


@_attrs_define
class EventExecutionEmitterResponse:
    """Non-secret historical execution attribution. Requester and queue-item
    attribution stay behind their own inspection permissions.

        Attributes:
            action_ref (str):
            admission_id (int):
            attempt (UUID):
            execution_id (int):
            pack_id (int):
            pack_ref (str):
            policy_revision_id (int):
            release_digest (str):
            release_id (int):
            sponsor_identity_id (int):
    """

    action_ref: str
    admission_id: int
    attempt: UUID
    execution_id: int
    pack_id: int
    pack_ref: str
    policy_revision_id: int
    release_digest: str
    release_id: int
    sponsor_identity_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_ref = self.action_ref

        admission_id = self.admission_id

        attempt = str(self.attempt)

        execution_id = self.execution_id

        pack_id = self.pack_id

        pack_ref = self.pack_ref

        policy_revision_id = self.policy_revision_id

        release_digest = self.release_digest

        release_id = self.release_id

        sponsor_identity_id = self.sponsor_identity_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action_ref": action_ref,
                "admission_id": admission_id,
                "attempt": attempt,
                "execution_id": execution_id,
                "pack_id": pack_id,
                "pack_ref": pack_ref,
                "policy_revision_id": policy_revision_id,
                "release_digest": release_digest,
                "release_id": release_id,
                "sponsor_identity_id": sponsor_identity_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        action_ref = d.pop("action_ref")

        admission_id = d.pop("admission_id")

        attempt = UUID(d.pop("attempt"))

        execution_id = d.pop("execution_id")

        pack_id = d.pop("pack_id")

        pack_ref = d.pop("pack_ref")

        policy_revision_id = d.pop("policy_revision_id")

        release_digest = d.pop("release_digest")

        release_id = d.pop("release_id")

        sponsor_identity_id = d.pop("sponsor_identity_id")

        event_execution_emitter_response = cls(
            action_ref=action_ref,
            admission_id=admission_id,
            attempt=attempt,
            execution_id=execution_id,
            pack_id=pack_id,
            pack_ref=pack_ref,
            policy_revision_id=policy_revision_id,
            release_digest=release_digest,
            release_id=release_id,
            sponsor_identity_id=sponsor_identity_id,
        )

        event_execution_emitter_response.additional_properties = d
        return event_execution_emitter_response

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

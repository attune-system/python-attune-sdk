from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SensorRuntimeRevocationRequest")


@_attrs_define
class SensorRuntimeRevocationRequest:
    """Explicit operational revocation, separate from disablement or human IAM edits.

    Attributes:
        metadata_revision (int | None | Unset): Revoke only this immutable revision. Omit to revoke every sensor
            generation.
    """

    metadata_revision: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        metadata_revision: int | None | Unset
        if isinstance(self.metadata_revision, Unset):
            metadata_revision = UNSET
        else:
            metadata_revision = self.metadata_revision

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if metadata_revision is not UNSET:
            field_dict["metadata_revision"] = metadata_revision

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_metadata_revision(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        metadata_revision = _parse_metadata_revision(d.pop("metadata_revision", UNSET))

        sensor_runtime_revocation_request = cls(
            metadata_revision=metadata_revision,
        )

        return sensor_runtime_revocation_request

from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.log_availability_state import LogAvailabilityState
from ..types import UNSET, Unset

T = TypeVar("T", bound="LogAvailability")


@_attrs_define
class LogAvailability:
    """
    Attributes:
        state (LogAvailabilityState):
        artifact_version (int | None | Unset):
        finalize_by (datetime.datetime | None | Unset):
        retry_after_ms (int | None | Unset):
        revision (int | None | Unset):
        stream (int | None | Unset):
    """

    state: LogAvailabilityState
    artifact_version: int | None | Unset = UNSET
    finalize_by: datetime.datetime | None | Unset = UNSET
    retry_after_ms: int | None | Unset = UNSET
    revision: int | None | Unset = UNSET
    stream: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state.value

        artifact_version: int | None | Unset
        if isinstance(self.artifact_version, Unset):
            artifact_version = UNSET
        else:
            artifact_version = self.artifact_version

        finalize_by: None | str | Unset
        if isinstance(self.finalize_by, Unset):
            finalize_by = UNSET
        elif isinstance(self.finalize_by, datetime.datetime):
            finalize_by = self.finalize_by.isoformat()
        else:
            finalize_by = self.finalize_by

        retry_after_ms: int | None | Unset
        if isinstance(self.retry_after_ms, Unset):
            retry_after_ms = UNSET
        else:
            retry_after_ms = self.retry_after_ms

        revision: int | None | Unset
        if isinstance(self.revision, Unset):
            revision = UNSET
        else:
            revision = self.revision

        stream: int | None | Unset
        if isinstance(self.stream, Unset):
            stream = UNSET
        else:
            stream = self.stream

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
            }
        )
        if artifact_version is not UNSET:
            field_dict["artifact_version"] = artifact_version
        if finalize_by is not UNSET:
            field_dict["finalize_by"] = finalize_by
        if retry_after_ms is not UNSET:
            field_dict["retry_after_ms"] = retry_after_ms
        if revision is not UNSET:
            field_dict["revision"] = revision
        if stream is not UNSET:
            field_dict["stream"] = stream

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        state = LogAvailabilityState(d.pop("state"))

        def _parse_artifact_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        artifact_version = _parse_artifact_version(d.pop("artifact_version", UNSET))

        def _parse_finalize_by(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finalize_by_type_0 = datetime.datetime.fromisoformat(data)

                return finalize_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        finalize_by = _parse_finalize_by(d.pop("finalize_by", UNSET))

        def _parse_retry_after_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        retry_after_ms = _parse_retry_after_ms(d.pop("retry_after_ms", UNSET))

        def _parse_revision(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        revision = _parse_revision(d.pop("revision", UNSET))

        def _parse_stream(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        stream = _parse_stream(d.pop("stream", UNSET))

        log_availability = cls(
            state=state,
            artifact_version=artifact_version,
            finalize_by=finalize_by,
            retry_after_ms=retry_after_ms,
            revision=revision,
            stream=stream,
        )

        log_availability.additional_properties = d
        return log_availability

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

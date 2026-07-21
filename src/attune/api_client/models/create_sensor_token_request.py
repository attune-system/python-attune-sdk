from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateSensorTokenRequest")


@_attrs_define
class CreateSensorTokenRequest:
    """Request body for creating sensor tokens

    Attributes:
        sensor_ref (str): Sensor reference (e.g., "core.timer")
        trigger_types (list[str]): List of trigger types this sensor can create events for
        ttl_seconds (int | None | Unset): Optional TTL in seconds (default: 86400 = 24 hours, max: 259200 = 72 hours)
    """

    sensor_ref: str
    trigger_types: list[str]
    ttl_seconds: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sensor_ref = self.sensor_ref

        trigger_types = self.trigger_types

        ttl_seconds: int | None | Unset
        if isinstance(self.ttl_seconds, Unset):
            ttl_seconds = UNSET
        else:
            ttl_seconds = self.ttl_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sensor_ref": sensor_ref,
                "trigger_types": trigger_types,
            }
        )
        if ttl_seconds is not UNSET:
            field_dict["ttl_seconds"] = ttl_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sensor_ref = d.pop("sensor_ref")

        trigger_types = cast(list[str], d.pop("trigger_types"))

        def _parse_ttl_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        ttl_seconds = _parse_ttl_seconds(d.pop("ttl_seconds", UNSET))

        create_sensor_token_request = cls(
            sensor_ref=sensor_ref,
            trigger_types=trigger_types,
            ttl_seconds=ttl_seconds,
        )

        create_sensor_token_request.additional_properties = d
        return create_sensor_token_request

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

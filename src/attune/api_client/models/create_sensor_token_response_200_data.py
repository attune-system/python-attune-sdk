from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateSensorTokenResponse200Data")


@_attrs_define
class CreateSensorTokenResponse200Data:
    """Response for sensor token creation

    Attributes:
        expires_at (str):
        identity_id (int):
        sensor_ref (str):
        token (str):
        trigger_types (list[str]):
    """

    expires_at: str
    identity_id: int
    sensor_ref: str
    token: str
    trigger_types: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expires_at = self.expires_at

        identity_id = self.identity_id

        sensor_ref = self.sensor_ref

        token = self.token

        trigger_types = self.trigger_types

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expires_at": expires_at,
                "identity_id": identity_id,
                "sensor_ref": sensor_ref,
                "token": token,
                "trigger_types": trigger_types,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expires_at = d.pop("expires_at")

        identity_id = d.pop("identity_id")

        sensor_ref = d.pop("sensor_ref")

        token = d.pop("token")

        trigger_types = cast(list[str], d.pop("trigger_types"))

        create_sensor_token_response_200_data = cls(
            expires_at=expires_at,
            identity_id=identity_id,
            sensor_ref=sensor_ref,
            token=token,
            trigger_types=trigger_types,
        )

        create_sensor_token_response_200_data.additional_properties = d
        return create_sensor_token_response_200_data

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DownloadPacksRequest")


@_attrs_define
class DownloadPacksRequest:
    """Request DTO for downloading packs

    Attributes:
        destination_dir (str): Destination directory for downloaded packs Example: /tmp/attune-packs.
        packs (list[str]): List of pack sources (git URLs, HTTP URLs, or registry refs) Example:
            ['https://github.com/attune/pack-slack.git', 'aws@2.0.0'].
        ref_spec (None | str | Unset): Git reference (branch, tag, or commit) for git sources Example: v1.0.0.
        registry_url (None | str | Unset): Pack registry URL for resolving references Example:
            https://registry.attune.io/index.json.
        timeout (int | Unset): Download timeout in seconds Example: 300.
        verify_ssl (bool | Unset): Verify SSL certificates Example: True.
    """

    destination_dir: str
    packs: list[str]
    ref_spec: None | str | Unset = UNSET
    registry_url: None | str | Unset = UNSET
    timeout: int | Unset = UNSET
    verify_ssl: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destination_dir = self.destination_dir

        packs = self.packs

        ref_spec: None | str | Unset
        if isinstance(self.ref_spec, Unset):
            ref_spec = UNSET
        else:
            ref_spec = self.ref_spec

        registry_url: None | str | Unset
        if isinstance(self.registry_url, Unset):
            registry_url = UNSET
        else:
            registry_url = self.registry_url

        timeout = self.timeout

        verify_ssl = self.verify_ssl

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "destination_dir": destination_dir,
                "packs": packs,
            }
        )
        if ref_spec is not UNSET:
            field_dict["ref_spec"] = ref_spec
        if registry_url is not UNSET:
            field_dict["registry_url"] = registry_url
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if verify_ssl is not UNSET:
            field_dict["verify_ssl"] = verify_ssl

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        destination_dir = d.pop("destination_dir")

        packs = cast(list[str], d.pop("packs"))

        def _parse_ref_spec(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ref_spec = _parse_ref_spec(d.pop("ref_spec", UNSET))

        def _parse_registry_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        registry_url = _parse_registry_url(d.pop("registry_url", UNSET))

        timeout = d.pop("timeout", UNSET)

        verify_ssl = d.pop("verify_ssl", UNSET)

        download_packs_request = cls(
            destination_dir=destination_dir,
            packs=packs,
            ref_spec=ref_spec,
            registry_url=registry_url,
            timeout=timeout,
            verify_ssl=verify_ssl,
        )

        download_packs_request.additional_properties = d
        return download_packs_request

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

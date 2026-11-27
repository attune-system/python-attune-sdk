from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="BrandingConfig")


@_attrs_define
class BrandingConfig:
    """Public image URLs for installation branding in the web UI.

    Attributes:
        favicon_url (None | str | Unset): Browser tab icon.
        icon_url (None | str | Unset): Compact logo for the collapsed sidebar.
        logo_url (None | str | Unset): Logo for the sign-in page and expanded sidebar.
        workflow_watermark_url (None | str | Unset): Tiled watermark for the workflow builder canvas.
    """

    favicon_url: None | str | Unset = UNSET
    icon_url: None | str | Unset = UNSET
    logo_url: None | str | Unset = UNSET
    workflow_watermark_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        favicon_url: None | str | Unset
        if isinstance(self.favicon_url, Unset):
            favicon_url = UNSET
        else:
            favicon_url = self.favicon_url

        icon_url: None | str | Unset
        if isinstance(self.icon_url, Unset):
            icon_url = UNSET
        else:
            icon_url = self.icon_url

        logo_url: None | str | Unset
        if isinstance(self.logo_url, Unset):
            logo_url = UNSET
        else:
            logo_url = self.logo_url

        workflow_watermark_url: None | str | Unset
        if isinstance(self.workflow_watermark_url, Unset):
            workflow_watermark_url = UNSET
        else:
            workflow_watermark_url = self.workflow_watermark_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if favicon_url is not UNSET:
            field_dict["favicon_url"] = favicon_url
        if icon_url is not UNSET:
            field_dict["icon_url"] = icon_url
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url
        if workflow_watermark_url is not UNSET:
            field_dict["workflow_watermark_url"] = workflow_watermark_url

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_favicon_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        favicon_url = _parse_favicon_url(d.pop("favicon_url", UNSET))

        def _parse_icon_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        icon_url = _parse_icon_url(d.pop("icon_url", UNSET))

        def _parse_logo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logo_url = _parse_logo_url(d.pop("logo_url", UNSET))

        def _parse_workflow_watermark_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        workflow_watermark_url = _parse_workflow_watermark_url(
            d.pop("workflow_watermark_url", UNSET)
        )

        branding_config = cls(
            favicon_url=favicon_url,
            icon_url=icon_url,
            logo_url=logo_url,
            workflow_watermark_url=workflow_watermark_url,
        )

        branding_config.additional_properties = d
        return branding_config

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

from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.permission_grant_definition import PermissionGrantDefinition


T = TypeVar("T", bound="RendererInputApprovalRequest")


@_attrs_define
class RendererInputApprovalRequest:
    """
    Attributes:
        declaration_revision (str):
        expression (str):
        grants (list[PermissionGrantDefinition]):
        renderer_execution (int): Convenience target for an already admitted renderer, not a policy target.
        source_path (str):
        expires_at (datetime.datetime | None | Unset):
    """

    declaration_revision: str
    expression: str
    grants: list[PermissionGrantDefinition]
    renderer_execution: int
    source_path: str
    expires_at: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        declaration_revision = self.declaration_revision

        expression = self.expression

        grants = []
        for grants_item_data in self.grants:
            grants_item = grants_item_data.to_dict()
            grants.append(grants_item)

        renderer_execution = self.renderer_execution

        source_path = self.source_path

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "declaration_revision": declaration_revision,
                "expression": expression,
                "grants": grants,
                "renderer_execution": renderer_execution,
                "source_path": source_path,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.permission_grant_definition import PermissionGrantDefinition

        d = dict(src_dict)
        declaration_revision = d.pop("declaration_revision")

        expression = d.pop("expression")

        grants = []
        _grants = d.pop("grants")
        for grants_item_data in _grants:
            grants_item = PermissionGrantDefinition.from_dict(grants_item_data)

            grants.append(grants_item)

        renderer_execution = d.pop("renderer_execution")

        source_path = d.pop("source_path")

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = datetime.datetime.fromisoformat(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        renderer_input_approval_request = cls(
            declaration_revision=declaration_revision,
            expression=expression,
            grants=grants,
            renderer_execution=renderer_execution,
            source_path=source_path,
            expires_at=expires_at,
        )

        return renderer_input_approval_request

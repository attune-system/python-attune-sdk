from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.permission_scope import PermissionScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatePermissionSetRequest")


@_attrs_define
class CreatePermissionSetRequest:
    """
    Attributes:
        grants (Any):
        ref (str): Unique reference in namespace.name format. Does not imply pack ownership.
        description (None | str | Unset):
        label (None | str | Unset):
        scope (None | PermissionScope | Unset):
    """

    grants: Any
    ref: str
    description: None | str | Unset = UNSET
    label: None | str | Unset = UNSET
    scope: None | PermissionScope | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        grants = self.grants

        ref = self.ref

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        scope: None | str | Unset
        if isinstance(self.scope, Unset):
            scope = UNSET
        elif isinstance(self.scope, PermissionScope):
            scope = self.scope.value
        else:
            scope = self.scope

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "grants": grants,
                "ref": ref,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if label is not UNSET:
            field_dict["label"] = label
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        grants = d.pop("grants")

        ref = d.pop("ref")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_scope(data: object) -> None | PermissionScope | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_1 = PermissionScope(data)

                return scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PermissionScope | Unset, data)

        scope = _parse_scope(d.pop("scope", UNSET))

        create_permission_set_request = cls(
            grants=grants,
            ref=ref,
            description=description,
            label=label,
            scope=scope,
        )

        return create_permission_set_request

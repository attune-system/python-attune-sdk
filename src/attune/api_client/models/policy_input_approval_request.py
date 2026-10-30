from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.invocation_binding_type_0 import InvocationBindingType0
    from ..models.invocation_binding_type_1 import InvocationBindingType1
    from ..models.invocation_binding_type_2 import InvocationBindingType2
    from ..models.invocation_binding_type_3 import InvocationBindingType3
    from ..models.permission_grant_definition import PermissionGrantDefinition


T = TypeVar("T", bound="PolicyInputApprovalRequest")


@_attrs_define
class PolicyInputApprovalRequest:
    """
    Attributes:
        declaration_revision (str):
        expression (str):
        grants (list[PermissionGrantDefinition]):
        invocation_binding (InvocationBindingType0 | InvocationBindingType1 | InvocationBindingType2 |
            InvocationBindingType3):
        policy_revision (int): Pre-execution target, supplied with invocation_binding, without a renderer.
        source_path (str):
        expires_at (datetime.datetime | None | Unset):
    """

    declaration_revision: str
    expression: str
    grants: list[PermissionGrantDefinition]
    invocation_binding: (
        InvocationBindingType0
        | InvocationBindingType1
        | InvocationBindingType2
        | InvocationBindingType3
    )
    policy_revision: int
    source_path: str
    expires_at: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.invocation_binding_type_0 import InvocationBindingType0
        from ..models.invocation_binding_type_1 import InvocationBindingType1
        from ..models.invocation_binding_type_2 import InvocationBindingType2

        declaration_revision = self.declaration_revision

        expression = self.expression

        grants = []
        for grants_item_data in self.grants:
            grants_item = grants_item_data.to_dict()
            grants.append(grants_item)

        invocation_binding: dict[str, Any]
        if (
            isinstance(self.invocation_binding, InvocationBindingType0)
            or isinstance(self.invocation_binding, InvocationBindingType1)
            or isinstance(self.invocation_binding, InvocationBindingType2)
        ):
            invocation_binding = self.invocation_binding.to_dict()
        else:
            invocation_binding = self.invocation_binding.to_dict()

        policy_revision = self.policy_revision

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
                "invocation_binding": invocation_binding,
                "policy_revision": policy_revision,
                "source_path": source_path,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.invocation_binding_type_0 import InvocationBindingType0
        from ..models.invocation_binding_type_1 import InvocationBindingType1
        from ..models.invocation_binding_type_2 import InvocationBindingType2
        from ..models.invocation_binding_type_3 import InvocationBindingType3
        from ..models.permission_grant_definition import PermissionGrantDefinition

        d = dict(src_dict)
        declaration_revision = d.pop("declaration_revision")

        expression = d.pop("expression")

        grants = []
        _grants = d.pop("grants")
        for grants_item_data in _grants:
            grants_item = PermissionGrantDefinition.from_dict(grants_item_data)

            grants.append(grants_item)

        def _parse_invocation_binding(
            data: object,
        ) -> (
            InvocationBindingType0
            | InvocationBindingType1
            | InvocationBindingType2
            | InvocationBindingType3
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_invocation_binding_type_0 = (
                    InvocationBindingType0.from_dict(data)
                )

                return componentsschemas_invocation_binding_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_invocation_binding_type_1 = (
                    InvocationBindingType1.from_dict(data)
                )

                return componentsschemas_invocation_binding_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_invocation_binding_type_2 = (
                    InvocationBindingType2.from_dict(data)
                )

                return componentsschemas_invocation_binding_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_invocation_binding_type_3 = (
                InvocationBindingType3.from_dict(data)
            )

            return componentsschemas_invocation_binding_type_3

        invocation_binding = _parse_invocation_binding(d.pop("invocation_binding"))

        policy_revision = d.pop("policy_revision")

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

        policy_input_approval_request = cls(
            declaration_revision=declaration_revision,
            expression=expression,
            grants=grants,
            invocation_binding=invocation_binding,
            policy_revision=policy_revision,
            source_path=source_path,
            expires_at=expires_at,
        )

        return policy_input_approval_request

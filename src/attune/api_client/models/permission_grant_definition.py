from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.permission_scope import PermissionScope
from ..models.rbac_action import RbacAction
from ..models.rbac_resource import RbacResource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.authored_grant_constraints import AuthoredGrantConstraints


T = TypeVar("T", bound="PermissionGrantDefinition")


@_attrs_define
class PermissionGrantDefinition:
    """Canonical authored grant. A grant may override its set's default scope.

    Attributes:
        actions (list[RbacAction]):
        resource (RbacResource):
        constraints (AuthoredGrantConstraints | None | Unset):
        scope (None | PermissionScope | Unset):
    """

    actions: list[RbacAction]
    resource: RbacResource
    constraints: AuthoredGrantConstraints | None | Unset = UNSET
    scope: None | PermissionScope | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.authored_grant_constraints import AuthoredGrantConstraints

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.value
            actions.append(actions_item)

        resource = self.resource.value

        constraints: dict[str, Any] | None | Unset
        if isinstance(self.constraints, Unset):
            constraints = UNSET
        elif isinstance(self.constraints, AuthoredGrantConstraints):
            constraints = self.constraints.to_dict()
        else:
            constraints = self.constraints

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
                "actions": actions,
                "resource": resource,
            }
        )
        if constraints is not UNSET:
            field_dict["constraints"] = constraints
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.authored_grant_constraints import AuthoredGrantConstraints

        d = dict(src_dict)
        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = RbacAction(actions_item_data)

            actions.append(actions_item)

        resource = RbacResource(d.pop("resource"))

        def _parse_constraints(data: object) -> AuthoredGrantConstraints | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                constraints_type_1 = AuthoredGrantConstraints.from_dict(data)

                return constraints_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AuthoredGrantConstraints | None | Unset, data)

        constraints = _parse_constraints(d.pop("constraints", UNSET))

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

        permission_grant_definition = cls(
            actions=actions,
            resource=resource,
            constraints=constraints,
            scope=scope,
        )

        return permission_grant_definition

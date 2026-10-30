from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.rbac_action import RbacAction
from ..models.rbac_resource import RbacResource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rbac_grant_constraints import RbacGrantConstraints


T = TypeVar("T", bound="RbacGrant")


@_attrs_define
class RbacGrant:
    """
    Attributes:
        actions (list[RbacAction]):
        resource (RbacResource):
        constraints (None | RbacGrantConstraints | Unset):
    """

    actions: list[RbacAction]
    resource: RbacResource
    constraints: None | RbacGrantConstraints | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.rbac_grant_constraints import RbacGrantConstraints

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.value
            actions.append(actions_item)

        resource = self.resource.value

        constraints: dict[str, Any] | None | Unset
        if isinstance(self.constraints, Unset):
            constraints = UNSET
        elif isinstance(self.constraints, RbacGrantConstraints):
            constraints = self.constraints.to_dict()
        else:
            constraints = self.constraints

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "actions": actions,
                "resource": resource,
            }
        )
        if constraints is not UNSET:
            field_dict["constraints"] = constraints

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.rbac_grant_constraints import RbacGrantConstraints

        d = dict(src_dict)
        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = RbacAction(actions_item_data)

            actions.append(actions_item)

        resource = RbacResource(d.pop("resource"))

        def _parse_constraints(data: object) -> None | RbacGrantConstraints | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                constraints_type_1 = RbacGrantConstraints.from_dict(data)

                return constraints_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RbacGrantConstraints | Unset, data)

        constraints = _parse_constraints(d.pop("constraints", UNSET))

        rbac_grant = cls(
            actions=actions,
            resource=resource,
            constraints=constraints,
        )

        return rbac_grant

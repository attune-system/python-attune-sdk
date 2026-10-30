from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.artifact_visibility import ArtifactVisibility
from ..models.owner_type import OwnerType
from ..models.rbac_execution_scope_constraint import RbacExecutionScopeConstraint
from ..models.rbac_owner_constraint import RbacOwnerConstraint
from ..models.rbac_pack_owner_constraint import RbacPackOwnerConstraint
from ..models.rbac_pack_state_constraint import RbacPackStateConstraint
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rbac_grant_constraints_attributes_type_0 import (
        RbacGrantConstraintsAttributesType0,
    )


T = TypeVar("T", bound="RbacGrantConstraints")


@_attrs_define
class RbacGrantConstraints:
    """
    Attributes:
        attributes (None | RbacGrantConstraintsAttributesType0 | Unset):
        encrypted (bool | None | Unset):
        execution_scope (None | RbacExecutionScopeConstraint | Unset):
        ids (list[int] | None | Unset):
        managing_pack_id (int | None | Unset):
        owner (None | RbacOwnerConstraint | Unset):
        owner_refs (list[str] | None | Unset):
        owner_types (list[OwnerType] | None | Unset):
        pack_owner (None | RbacPackOwnerConstraint | Unset):
        pack_refs (list[str] | None | Unset):
        pack_state (None | RbacPackStateConstraint | Unset):
        refs (list[str] | None | Unset):
        visibility (list[ArtifactVisibility] | None | Unset):
    """

    attributes: None | RbacGrantConstraintsAttributesType0 | Unset = UNSET
    encrypted: bool | None | Unset = UNSET
    execution_scope: None | RbacExecutionScopeConstraint | Unset = UNSET
    ids: list[int] | None | Unset = UNSET
    managing_pack_id: int | None | Unset = UNSET
    owner: None | RbacOwnerConstraint | Unset = UNSET
    owner_refs: list[str] | None | Unset = UNSET
    owner_types: list[OwnerType] | None | Unset = UNSET
    pack_owner: None | RbacPackOwnerConstraint | Unset = UNSET
    pack_refs: list[str] | None | Unset = UNSET
    pack_state: None | RbacPackStateConstraint | Unset = UNSET
    refs: list[str] | None | Unset = UNSET
    visibility: list[ArtifactVisibility] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.rbac_grant_constraints_attributes_type_0 import (
            RbacGrantConstraintsAttributesType0,
        )

        attributes: dict[str, Any] | None | Unset
        if isinstance(self.attributes, Unset):
            attributes = UNSET
        elif isinstance(self.attributes, RbacGrantConstraintsAttributesType0):
            attributes = self.attributes.to_dict()
        else:
            attributes = self.attributes

        encrypted: bool | None | Unset
        if isinstance(self.encrypted, Unset):
            encrypted = UNSET
        else:
            encrypted = self.encrypted

        execution_scope: None | str | Unset
        if isinstance(self.execution_scope, Unset):
            execution_scope = UNSET
        elif isinstance(self.execution_scope, RbacExecutionScopeConstraint):
            execution_scope = self.execution_scope.value
        else:
            execution_scope = self.execution_scope

        ids: list[int] | None | Unset
        if isinstance(self.ids, Unset):
            ids = UNSET
        elif isinstance(self.ids, list):
            ids = self.ids

        else:
            ids = self.ids

        managing_pack_id: int | None | Unset
        if isinstance(self.managing_pack_id, Unset):
            managing_pack_id = UNSET
        else:
            managing_pack_id = self.managing_pack_id

        owner: None | str | Unset
        if isinstance(self.owner, Unset):
            owner = UNSET
        elif isinstance(self.owner, RbacOwnerConstraint):
            owner = self.owner.value
        else:
            owner = self.owner

        owner_refs: list[str] | None | Unset
        if isinstance(self.owner_refs, Unset):
            owner_refs = UNSET
        elif isinstance(self.owner_refs, list):
            owner_refs = self.owner_refs

        else:
            owner_refs = self.owner_refs

        owner_types: list[str] | None | Unset
        if isinstance(self.owner_types, Unset):
            owner_types = UNSET
        elif isinstance(self.owner_types, list):
            owner_types = []
            for owner_types_type_0_item_data in self.owner_types:
                owner_types_type_0_item = owner_types_type_0_item_data.value
                owner_types.append(owner_types_type_0_item)

        else:
            owner_types = self.owner_types

        pack_owner: None | str | Unset
        if isinstance(self.pack_owner, Unset):
            pack_owner = UNSET
        elif isinstance(self.pack_owner, RbacPackOwnerConstraint):
            pack_owner = self.pack_owner.value
        else:
            pack_owner = self.pack_owner

        pack_refs: list[str] | None | Unset
        if isinstance(self.pack_refs, Unset):
            pack_refs = UNSET
        elif isinstance(self.pack_refs, list):
            pack_refs = self.pack_refs

        else:
            pack_refs = self.pack_refs

        pack_state: None | str | Unset
        if isinstance(self.pack_state, Unset):
            pack_state = UNSET
        elif isinstance(self.pack_state, RbacPackStateConstraint):
            pack_state = self.pack_state.value
        else:
            pack_state = self.pack_state

        refs: list[str] | None | Unset
        if isinstance(self.refs, Unset):
            refs = UNSET
        elif isinstance(self.refs, list):
            refs = self.refs

        else:
            refs = self.refs

        visibility: list[str] | None | Unset
        if isinstance(self.visibility, Unset):
            visibility = UNSET
        elif isinstance(self.visibility, list):
            visibility = []
            for visibility_type_0_item_data in self.visibility:
                visibility_type_0_item = visibility_type_0_item_data.value
                visibility.append(visibility_type_0_item)

        else:
            visibility = self.visibility

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if encrypted is not UNSET:
            field_dict["encrypted"] = encrypted
        if execution_scope is not UNSET:
            field_dict["execution_scope"] = execution_scope
        if ids is not UNSET:
            field_dict["ids"] = ids
        if managing_pack_id is not UNSET:
            field_dict["managing_pack_id"] = managing_pack_id
        if owner is not UNSET:
            field_dict["owner"] = owner
        if owner_refs is not UNSET:
            field_dict["owner_refs"] = owner_refs
        if owner_types is not UNSET:
            field_dict["owner_types"] = owner_types
        if pack_owner is not UNSET:
            field_dict["pack_owner"] = pack_owner
        if pack_refs is not UNSET:
            field_dict["pack_refs"] = pack_refs
        if pack_state is not UNSET:
            field_dict["pack_state"] = pack_state
        if refs is not UNSET:
            field_dict["refs"] = refs
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.rbac_grant_constraints_attributes_type_0 import (
            RbacGrantConstraintsAttributesType0,
        )

        d = dict(src_dict)

        def _parse_attributes(
            data: object,
        ) -> None | RbacGrantConstraintsAttributesType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                attributes_type_0 = RbacGrantConstraintsAttributesType0.from_dict(data)

                return attributes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RbacGrantConstraintsAttributesType0 | Unset, data)

        attributes = _parse_attributes(d.pop("attributes", UNSET))

        def _parse_encrypted(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        encrypted = _parse_encrypted(d.pop("encrypted", UNSET))

        def _parse_execution_scope(
            data: object,
        ) -> None | RbacExecutionScopeConstraint | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                execution_scope_type_1 = RbacExecutionScopeConstraint(data)

                return execution_scope_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RbacExecutionScopeConstraint | Unset, data)

        execution_scope = _parse_execution_scope(d.pop("execution_scope", UNSET))

        def _parse_ids(data: object) -> list[int] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ids_type_0 = cast(list[int], data)

                return ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[int] | None | Unset, data)

        ids = _parse_ids(d.pop("ids", UNSET))

        def _parse_managing_pack_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        managing_pack_id = _parse_managing_pack_id(d.pop("managing_pack_id", UNSET))

        def _parse_owner(data: object) -> None | RbacOwnerConstraint | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                owner_type_1 = RbacOwnerConstraint(data)

                return owner_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RbacOwnerConstraint | Unset, data)

        owner = _parse_owner(d.pop("owner", UNSET))

        def _parse_owner_refs(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                owner_refs_type_0 = cast(list[str], data)

                return owner_refs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        owner_refs = _parse_owner_refs(d.pop("owner_refs", UNSET))

        def _parse_owner_types(data: object) -> list[OwnerType] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                owner_types_type_0 = []
                _owner_types_type_0 = data
                for owner_types_type_0_item_data in _owner_types_type_0:
                    owner_types_type_0_item = OwnerType(owner_types_type_0_item_data)

                    owner_types_type_0.append(owner_types_type_0_item)

                return owner_types_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[OwnerType] | None | Unset, data)

        owner_types = _parse_owner_types(d.pop("owner_types", UNSET))

        def _parse_pack_owner(data: object) -> None | RbacPackOwnerConstraint | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pack_owner_type_1 = RbacPackOwnerConstraint(data)

                return pack_owner_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RbacPackOwnerConstraint | Unset, data)

        pack_owner = _parse_pack_owner(d.pop("pack_owner", UNSET))

        def _parse_pack_refs(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                pack_refs_type_0 = cast(list[str], data)

                return pack_refs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        pack_refs = _parse_pack_refs(d.pop("pack_refs", UNSET))

        def _parse_pack_state(data: object) -> None | RbacPackStateConstraint | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pack_state_type_1 = RbacPackStateConstraint(data)

                return pack_state_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RbacPackStateConstraint | Unset, data)

        pack_state = _parse_pack_state(d.pop("pack_state", UNSET))

        def _parse_refs(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                refs_type_0 = cast(list[str], data)

                return refs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        refs = _parse_refs(d.pop("refs", UNSET))

        def _parse_visibility(data: object) -> list[ArtifactVisibility] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                visibility_type_0 = []
                _visibility_type_0 = data
                for visibility_type_0_item_data in _visibility_type_0:
                    visibility_type_0_item = ArtifactVisibility(
                        visibility_type_0_item_data
                    )

                    visibility_type_0.append(visibility_type_0_item)

                return visibility_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ArtifactVisibility] | None | Unset, data)

        visibility = _parse_visibility(d.pop("visibility", UNSET))

        rbac_grant_constraints = cls(
            attributes=attributes,
            encrypted=encrypted,
            execution_scope=execution_scope,
            ids=ids,
            managing_pack_id=managing_pack_id,
            owner=owner,
            owner_refs=owner_refs,
            owner_types=owner_types,
            pack_owner=pack_owner,
            pack_refs=pack_refs,
            pack_state=pack_state,
            refs=refs,
            visibility=visibility,
        )

        return rbac_grant_constraints

from __future__ import annotations

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


T = TypeVar("T", bound="DeclaredInputApprovalTarget")


@_attrs_define
class DeclaredInputApprovalTarget:
    """
    Attributes:
        action_id (int):
        action_ref (str):
        declaration_revision (str):
        expression (str): Authored metadata only, never the evaluated input or source configuration.
        invocation_binding (InvocationBindingType0 | InvocationBindingType1 | InvocationBindingType2 |
            InvocationBindingType3):
        pack_id (int):
        pack_ref (str):
        policy_revision (int):
        release_id (int):
        source_path (str):
        metadata_revision (int | None | Unset):
    """

    action_id: int
    action_ref: str
    declaration_revision: str
    expression: str
    invocation_binding: (
        InvocationBindingType0
        | InvocationBindingType1
        | InvocationBindingType2
        | InvocationBindingType3
    )
    pack_id: int
    pack_ref: str
    policy_revision: int
    release_id: int
    source_path: str
    metadata_revision: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.invocation_binding_type_0 import InvocationBindingType0
        from ..models.invocation_binding_type_1 import InvocationBindingType1
        from ..models.invocation_binding_type_2 import InvocationBindingType2

        action_id = self.action_id

        action_ref = self.action_ref

        declaration_revision = self.declaration_revision

        expression = self.expression

        invocation_binding: dict[str, Any]
        if (
            isinstance(self.invocation_binding, InvocationBindingType0)
            or isinstance(self.invocation_binding, InvocationBindingType1)
            or isinstance(self.invocation_binding, InvocationBindingType2)
        ):
            invocation_binding = self.invocation_binding.to_dict()
        else:
            invocation_binding = self.invocation_binding.to_dict()

        pack_id = self.pack_id

        pack_ref = self.pack_ref

        policy_revision = self.policy_revision

        release_id = self.release_id

        source_path = self.source_path

        metadata_revision: int | None | Unset
        if isinstance(self.metadata_revision, Unset):
            metadata_revision = UNSET
        else:
            metadata_revision = self.metadata_revision

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "action_id": action_id,
                "action_ref": action_ref,
                "declaration_revision": declaration_revision,
                "expression": expression,
                "invocation_binding": invocation_binding,
                "pack_id": pack_id,
                "pack_ref": pack_ref,
                "policy_revision": policy_revision,
                "release_id": release_id,
                "source_path": source_path,
            }
        )
        if metadata_revision is not UNSET:
            field_dict["metadata_revision"] = metadata_revision

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.invocation_binding_type_0 import InvocationBindingType0
        from ..models.invocation_binding_type_1 import InvocationBindingType1
        from ..models.invocation_binding_type_2 import InvocationBindingType2
        from ..models.invocation_binding_type_3 import InvocationBindingType3

        d = dict(src_dict)
        action_id = d.pop("action_id")

        action_ref = d.pop("action_ref")

        declaration_revision = d.pop("declaration_revision")

        expression = d.pop("expression")

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

        pack_id = d.pop("pack_id")

        pack_ref = d.pop("pack_ref")

        policy_revision = d.pop("policy_revision")

        release_id = d.pop("release_id")

        source_path = d.pop("source_path")

        def _parse_metadata_revision(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        metadata_revision = _parse_metadata_revision(d.pop("metadata_revision", UNSET))

        declared_input_approval_target = cls(
            action_id=action_id,
            action_ref=action_ref,
            declaration_revision=declaration_revision,
            expression=expression,
            invocation_binding=invocation_binding,
            pack_id=pack_id,
            pack_ref=pack_ref,
            policy_revision=policy_revision,
            release_id=release_id,
            source_path=source_path,
            metadata_revision=metadata_revision,
        )

        return declared_input_approval_target

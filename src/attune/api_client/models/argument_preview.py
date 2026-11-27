from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cli_binding_type_0 import CliBindingType0
    from ..models.cli_binding_type_1 import CliBindingType1
    from ..models.cli_binding_type_2 import CliBindingType2


T = TypeVar("T", bound="ArgumentPreview")


@_attrs_define
class ArgumentPreview:
    """Definition-only preview. Contains no execution input or resolved secret value.

    Attributes:
        order (int):
        cli (CliBindingType0 | CliBindingType1 | CliBindingType2 | None | Unset):
        literal (None | str | Unset):
        parameter (None | str | Unset):
    """

    order: int
    cli: CliBindingType0 | CliBindingType1 | CliBindingType2 | None | Unset = UNSET
    literal: None | str | Unset = UNSET
    parameter: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cli_binding_type_0 import CliBindingType0
        from ..models.cli_binding_type_1 import CliBindingType1
        from ..models.cli_binding_type_2 import CliBindingType2

        order = self.order

        cli: dict[str, Any] | None | Unset
        if isinstance(self.cli, Unset):
            cli = UNSET
        elif (
            isinstance(self.cli, CliBindingType0)
            or isinstance(self.cli, CliBindingType1)
            or isinstance(self.cli, CliBindingType2)
        ):
            cli = self.cli.to_dict()
        else:
            cli = self.cli

        literal: None | str | Unset
        if isinstance(self.literal, Unset):
            literal = UNSET
        else:
            literal = self.literal

        parameter: None | str | Unset
        if isinstance(self.parameter, Unset):
            parameter = UNSET
        else:
            parameter = self.parameter

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "order": order,
            }
        )
        if cli is not UNSET:
            field_dict["cli"] = cli
        if literal is not UNSET:
            field_dict["literal"] = literal
        if parameter is not UNSET:
            field_dict["parameter"] = parameter

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.cli_binding_type_0 import CliBindingType0
        from ..models.cli_binding_type_1 import CliBindingType1
        from ..models.cli_binding_type_2 import CliBindingType2

        d = dict(src_dict)
        order = d.pop("order")

        def _parse_cli(
            data: object,
        ) -> CliBindingType0 | CliBindingType1 | CliBindingType2 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_cli_binding_type_0 = CliBindingType0.from_dict(data)

                return componentsschemas_cli_binding_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_cli_binding_type_1 = CliBindingType1.from_dict(data)

                return componentsschemas_cli_binding_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_cli_binding_type_2 = CliBindingType2.from_dict(data)

                return componentsschemas_cli_binding_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CliBindingType0 | CliBindingType1 | CliBindingType2 | None | Unset, data
            )

        cli = _parse_cli(d.pop("cli", UNSET))

        def _parse_literal(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        literal = _parse_literal(d.pop("literal", UNSET))

        def _parse_parameter(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parameter = _parse_parameter(d.pop("parameter", UNSET))

        argument_preview = cls(
            order=order,
            cli=cli,
            literal=literal,
            parameter=parameter,
        )

        argument_preview.additional_properties = d
        return argument_preview

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

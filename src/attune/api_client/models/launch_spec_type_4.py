from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.launch_spec_type_4_type import LaunchSpecType4Type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.classpath_entry_type_0 import ClasspathEntryType0
    from ..models.classpath_entry_type_1 import ClasspathEntryType1


T = TypeVar("T", bound="LaunchSpecType4")


@_attrs_define
class LaunchSpecType4:
    """
    Attributes:
        classpath (list[ClasspathEntryType0 | ClasspathEntryType1]):
        main_class (str):
        type_ (LaunchSpecType4Type):
        jvm_args (list[str] | Unset):
    """

    classpath: list[ClasspathEntryType0 | ClasspathEntryType1]
    main_class: str
    type_: LaunchSpecType4Type
    jvm_args: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.classpath_entry_type_0 import ClasspathEntryType0

        classpath = []
        for classpath_item_data in self.classpath:
            classpath_item: dict[str, Any]
            if isinstance(classpath_item_data, ClasspathEntryType0):
                classpath_item = classpath_item_data.to_dict()
            else:
                classpath_item = classpath_item_data.to_dict()

            classpath.append(classpath_item)

        main_class = self.main_class

        type_ = self.type_.value

        jvm_args: list[str] | Unset = UNSET
        if not isinstance(self.jvm_args, Unset):
            jvm_args = self.jvm_args

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "classpath": classpath,
                "main_class": main_class,
                "type": type_,
            }
        )
        if jvm_args is not UNSET:
            field_dict["jvm_args"] = jvm_args

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.classpath_entry_type_0 import ClasspathEntryType0
        from ..models.classpath_entry_type_1 import ClasspathEntryType1

        d = dict(src_dict)
        classpath = []
        _classpath = d.pop("classpath")
        for classpath_item_data in _classpath:

            def _parse_classpath_item(
                data: object,
            ) -> ClasspathEntryType0 | ClasspathEntryType1:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_classpath_entry_type_0 = (
                        ClasspathEntryType0.from_dict(data)
                    )

                    return componentsschemas_classpath_entry_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_classpath_entry_type_1 = (
                    ClasspathEntryType1.from_dict(data)
                )

                return componentsschemas_classpath_entry_type_1

            classpath_item = _parse_classpath_item(classpath_item_data)

            classpath.append(classpath_item)

        main_class = d.pop("main_class")

        type_ = LaunchSpecType4Type(d.pop("type"))

        jvm_args = cast(list[str], d.pop("jvm_args", UNSET))

        launch_spec_type_4 = cls(
            classpath=classpath,
            main_class=main_class,
            type_=type_,
            jvm_args=jvm_args,
        )

        launch_spec_type_4.additional_properties = d
        return launch_spec_type_4

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

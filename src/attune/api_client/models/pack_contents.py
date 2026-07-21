from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component_summary import ComponentSummary


T = TypeVar("T", bound="PackContents")


@_attrs_define
class PackContents:
    """Pack contents summary

    Attributes:
        actions (list[ComponentSummary] | Unset): List of actions
        rules (list[ComponentSummary] | Unset): List of bundled rules
        sensors (list[ComponentSummary] | Unset): List of sensors
        triggers (list[ComponentSummary] | Unset): List of triggers
        workflows (list[ComponentSummary] | Unset): List of bundled workflows
    """

    actions: list[ComponentSummary] | Unset = UNSET
    rules: list[ComponentSummary] | Unset = UNSET
    sensors: list[ComponentSummary] | Unset = UNSET
    triggers: list[ComponentSummary] | Unset = UNSET
    workflows: list[ComponentSummary] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)

        rules: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        sensors: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sensors, Unset):
            sensors = []
            for sensors_item_data in self.sensors:
                sensors_item = sensors_item_data.to_dict()
                sensors.append(sensors_item)

        triggers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.triggers, Unset):
            triggers = []
            for triggers_item_data in self.triggers:
                triggers_item = triggers_item_data.to_dict()
                triggers.append(triggers_item)

        workflows: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.workflows, Unset):
            workflows = []
            for workflows_item_data in self.workflows:
                workflows_item = workflows_item_data.to_dict()
                workflows.append(workflows_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if actions is not UNSET:
            field_dict["actions"] = actions
        if rules is not UNSET:
            field_dict["rules"] = rules
        if sensors is not UNSET:
            field_dict["sensors"] = sensors
        if triggers is not UNSET:
            field_dict["triggers"] = triggers
        if workflows is not UNSET:
            field_dict["workflows"] = workflows

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_summary import ComponentSummary

        d = dict(src_dict)
        _actions = d.pop("actions", UNSET)
        actions: list[ComponentSummary] | Unset = UNSET
        if _actions is not UNSET:
            actions = []
            for actions_item_data in _actions:
                actions_item = ComponentSummary.from_dict(actions_item_data)

                actions.append(actions_item)

        _rules = d.pop("rules", UNSET)
        rules: list[ComponentSummary] | Unset = UNSET
        if _rules is not UNSET:
            rules = []
            for rules_item_data in _rules:
                rules_item = ComponentSummary.from_dict(rules_item_data)

                rules.append(rules_item)

        _sensors = d.pop("sensors", UNSET)
        sensors: list[ComponentSummary] | Unset = UNSET
        if _sensors is not UNSET:
            sensors = []
            for sensors_item_data in _sensors:
                sensors_item = ComponentSummary.from_dict(sensors_item_data)

                sensors.append(sensors_item)

        _triggers = d.pop("triggers", UNSET)
        triggers: list[ComponentSummary] | Unset = UNSET
        if _triggers is not UNSET:
            triggers = []
            for triggers_item_data in _triggers:
                triggers_item = ComponentSummary.from_dict(triggers_item_data)

                triggers.append(triggers_item)

        _workflows = d.pop("workflows", UNSET)
        workflows: list[ComponentSummary] | Unset = UNSET
        if _workflows is not UNSET:
            workflows = []
            for workflows_item_data in _workflows:
                workflows_item = ComponentSummary.from_dict(workflows_item_data)

                workflows.append(workflows_item)

        pack_contents = cls(
            actions=actions,
            rules=rules,
            sensors=sensors,
            triggers=triggers,
            workflows=workflows,
        )

        pack_contents.additional_properties = d
        return pack_contents

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

from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.retention_policy_type import RetentionPolicyType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.paginated_response_action_summary_items_item_required_worker_runtimes import (
        PaginatedResponseActionSummaryItemsItemRequiredWorkerRuntimes,
    )
    from ..models.paginated_response_action_summary_items_item_worker_selector import (
        PaginatedResponseActionSummaryItemsItemWorkerSelector,
    )
    from ..models.worker_affinity import WorkerAffinity
    from ..models.worker_toleration import WorkerToleration


T = TypeVar("T", bound="PaginatedResponseActionSummaryItemsItem")


@_attrs_define
class PaginatedResponseActionSummaryItemsItem:
    """Simplified action response (for list endpoints)

    Attributes:
        accesses_mcp (bool): Hint that this action may invoke the Attune MCP server and spawn child executions. Default:
            False.
        created (datetime.datetime): Creation timestamp Example: 2024-01-13T10:30:00Z.
        entrypoint (str): Entry point Example: /actions/slack/post_message.py.
        id (int): Action ID Example: 1.
        label (str): Human-readable label Example: Post Message to Slack.
        pack_ref (str): Pack reference Example: slack.
        ref (str): Unique reference identifier Example: slack.post_message.
        updated (datetime.datetime): Last update timestamp Example: 2024-01-13T10:30:00Z.
        artifact_retention_limit (int | None | Unset): Per-action retention limit override for non-log artifacts created
            by executions. Example: 10.
        artifact_retention_policy (None | RetentionPolicyType | Unset):
        default_execution_permission_set_refs (list[str] | Unset): Default permission set refs used when executions do
            not explicitly override token permissions. Example: ['core.agent_reader'].
        description (None | str | Unset): Action description Example: Posts a message to a Slack channel.
        log_retention_limit (int | None | Unset): Per-action retention limit override for stdout/stderr execution log
            artifacts. Example: 4.
        log_retention_policy (None | RetentionPolicyType | Unset):
        required_worker_runtimes (PaginatedResponseActionSummaryItemsItemRequiredWorkerRuntimes | Unset): Additional
            worker runtime requirements keyed by runtime name/alias. Use "*" for any available version.
        runtime (int | None | Unset): Runtime ID Example: 1.
        runtime_ref (None | str | Unset): Runtime reference (stable identifier, e.g., "core.python") Example:
            core.python.
        runtime_version_constraint (None | str | Unset): Semver version constraint for the runtime Example: >=3.12.
        worker_affinity (WorkerAffinity | Unset):
        worker_selector (PaginatedResponseActionSummaryItemsItemWorkerSelector | Unset): Exact worker label
            requirements.
        worker_tolerations (list[WorkerToleration] | Unset): Tolerations for worker taints.
        workflow_def (int | None | Unset): Workflow definition ID (non-null if this action is a workflow) Example: 42.
    """

    created: datetime.datetime
    entrypoint: str
    id: int
    label: str
    pack_ref: str
    ref: str
    updated: datetime.datetime
    accesses_mcp: bool = False
    artifact_retention_limit: int | None | Unset = UNSET
    artifact_retention_policy: None | RetentionPolicyType | Unset = UNSET
    default_execution_permission_set_refs: list[str] | Unset = UNSET
    description: None | str | Unset = UNSET
    log_retention_limit: int | None | Unset = UNSET
    log_retention_policy: None | RetentionPolicyType | Unset = UNSET
    required_worker_runtimes: (
        PaginatedResponseActionSummaryItemsItemRequiredWorkerRuntimes | Unset
    ) = UNSET
    runtime: int | None | Unset = UNSET
    runtime_ref: None | str | Unset = UNSET
    runtime_version_constraint: None | str | Unset = UNSET
    worker_affinity: WorkerAffinity | Unset = UNSET
    worker_selector: PaginatedResponseActionSummaryItemsItemWorkerSelector | Unset = (
        UNSET
    )
    worker_tolerations: list[WorkerToleration] | Unset = UNSET
    workflow_def: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accesses_mcp = self.accesses_mcp

        created = self.created.isoformat()

        entrypoint = self.entrypoint

        id = self.id

        label = self.label

        pack_ref = self.pack_ref

        ref = self.ref

        updated = self.updated.isoformat()

        artifact_retention_limit: int | None | Unset
        if isinstance(self.artifact_retention_limit, Unset):
            artifact_retention_limit = UNSET
        else:
            artifact_retention_limit = self.artifact_retention_limit

        artifact_retention_policy: None | str | Unset
        if isinstance(self.artifact_retention_policy, Unset):
            artifact_retention_policy = UNSET
        elif isinstance(self.artifact_retention_policy, RetentionPolicyType):
            artifact_retention_policy = self.artifact_retention_policy.value
        else:
            artifact_retention_policy = self.artifact_retention_policy

        default_execution_permission_set_refs: list[str] | Unset = UNSET
        if not isinstance(self.default_execution_permission_set_refs, Unset):
            default_execution_permission_set_refs = (
                self.default_execution_permission_set_refs
            )

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        log_retention_limit: int | None | Unset
        if isinstance(self.log_retention_limit, Unset):
            log_retention_limit = UNSET
        else:
            log_retention_limit = self.log_retention_limit

        log_retention_policy: None | str | Unset
        if isinstance(self.log_retention_policy, Unset):
            log_retention_policy = UNSET
        elif isinstance(self.log_retention_policy, RetentionPolicyType):
            log_retention_policy = self.log_retention_policy.value
        else:
            log_retention_policy = self.log_retention_policy

        required_worker_runtimes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.required_worker_runtimes, Unset):
            required_worker_runtimes = self.required_worker_runtimes.to_dict()

        runtime: int | None | Unset
        if isinstance(self.runtime, Unset):
            runtime = UNSET
        else:
            runtime = self.runtime

        runtime_ref: None | str | Unset
        if isinstance(self.runtime_ref, Unset):
            runtime_ref = UNSET
        else:
            runtime_ref = self.runtime_ref

        runtime_version_constraint: None | str | Unset
        if isinstance(self.runtime_version_constraint, Unset):
            runtime_version_constraint = UNSET
        else:
            runtime_version_constraint = self.runtime_version_constraint

        worker_affinity: dict[str, Any] | Unset = UNSET
        if not isinstance(self.worker_affinity, Unset):
            worker_affinity = self.worker_affinity.to_dict()

        worker_selector: dict[str, Any] | Unset = UNSET
        if not isinstance(self.worker_selector, Unset):
            worker_selector = self.worker_selector.to_dict()

        worker_tolerations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.worker_tolerations, Unset):
            worker_tolerations = []
            for worker_tolerations_item_data in self.worker_tolerations:
                worker_tolerations_item = worker_tolerations_item_data.to_dict()
                worker_tolerations.append(worker_tolerations_item)

        workflow_def: int | None | Unset
        if isinstance(self.workflow_def, Unset):
            workflow_def = UNSET
        else:
            workflow_def = self.workflow_def

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accesses_mcp": accesses_mcp,
                "created": created,
                "entrypoint": entrypoint,
                "id": id,
                "label": label,
                "pack_ref": pack_ref,
                "ref": ref,
                "updated": updated,
            }
        )
        if artifact_retention_limit is not UNSET:
            field_dict["artifact_retention_limit"] = artifact_retention_limit
        if artifact_retention_policy is not UNSET:
            field_dict["artifact_retention_policy"] = artifact_retention_policy
        if default_execution_permission_set_refs is not UNSET:
            field_dict["default_execution_permission_set_refs"] = (
                default_execution_permission_set_refs
            )
        if description is not UNSET:
            field_dict["description"] = description
        if log_retention_limit is not UNSET:
            field_dict["log_retention_limit"] = log_retention_limit
        if log_retention_policy is not UNSET:
            field_dict["log_retention_policy"] = log_retention_policy
        if required_worker_runtimes is not UNSET:
            field_dict["required_worker_runtimes"] = required_worker_runtimes
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if runtime_ref is not UNSET:
            field_dict["runtime_ref"] = runtime_ref
        if runtime_version_constraint is not UNSET:
            field_dict["runtime_version_constraint"] = runtime_version_constraint
        if worker_affinity is not UNSET:
            field_dict["worker_affinity"] = worker_affinity
        if worker_selector is not UNSET:
            field_dict["worker_selector"] = worker_selector
        if worker_tolerations is not UNSET:
            field_dict["worker_tolerations"] = worker_tolerations
        if workflow_def is not UNSET:
            field_dict["workflow_def"] = workflow_def

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.paginated_response_action_summary_items_item_required_worker_runtimes import (
            PaginatedResponseActionSummaryItemsItemRequiredWorkerRuntimes,
        )
        from ..models.paginated_response_action_summary_items_item_worker_selector import (
            PaginatedResponseActionSummaryItemsItemWorkerSelector,
        )
        from ..models.worker_affinity import WorkerAffinity
        from ..models.worker_toleration import WorkerToleration

        d = dict(src_dict)
        accesses_mcp = d.pop("accesses_mcp")

        created = isoparse(d.pop("created"))

        entrypoint = d.pop("entrypoint")

        id = d.pop("id")

        label = d.pop("label")

        pack_ref = d.pop("pack_ref")

        ref = d.pop("ref")

        updated = isoparse(d.pop("updated"))

        def _parse_artifact_retention_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        artifact_retention_limit = _parse_artifact_retention_limit(
            d.pop("artifact_retention_limit", UNSET)
        )

        def _parse_artifact_retention_policy(
            data: object,
        ) -> None | RetentionPolicyType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                artifact_retention_policy_type_1 = RetentionPolicyType(data)

                return artifact_retention_policy_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RetentionPolicyType | Unset, data)

        artifact_retention_policy = _parse_artifact_retention_policy(
            d.pop("artifact_retention_policy", UNSET)
        )

        default_execution_permission_set_refs = cast(
            list[str], d.pop("default_execution_permission_set_refs", UNSET)
        )

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_log_retention_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        log_retention_limit = _parse_log_retention_limit(
            d.pop("log_retention_limit", UNSET)
        )

        def _parse_log_retention_policy(
            data: object,
        ) -> None | RetentionPolicyType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                log_retention_policy_type_1 = RetentionPolicyType(data)

                return log_retention_policy_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RetentionPolicyType | Unset, data)

        log_retention_policy = _parse_log_retention_policy(
            d.pop("log_retention_policy", UNSET)
        )

        _required_worker_runtimes = d.pop("required_worker_runtimes", UNSET)
        required_worker_runtimes: (
            PaginatedResponseActionSummaryItemsItemRequiredWorkerRuntimes | Unset
        )
        if isinstance(_required_worker_runtimes, Unset):
            required_worker_runtimes = UNSET
        else:
            required_worker_runtimes = (
                PaginatedResponseActionSummaryItemsItemRequiredWorkerRuntimes.from_dict(
                    _required_worker_runtimes
                )
            )

        def _parse_runtime(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        runtime = _parse_runtime(d.pop("runtime", UNSET))

        def _parse_runtime_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        runtime_ref = _parse_runtime_ref(d.pop("runtime_ref", UNSET))

        def _parse_runtime_version_constraint(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        runtime_version_constraint = _parse_runtime_version_constraint(
            d.pop("runtime_version_constraint", UNSET)
        )

        _worker_affinity = d.pop("worker_affinity", UNSET)
        worker_affinity: WorkerAffinity | Unset
        if isinstance(_worker_affinity, Unset):
            worker_affinity = UNSET
        else:
            worker_affinity = WorkerAffinity.from_dict(_worker_affinity)

        _worker_selector = d.pop("worker_selector", UNSET)
        worker_selector: PaginatedResponseActionSummaryItemsItemWorkerSelector | Unset
        if isinstance(_worker_selector, Unset):
            worker_selector = UNSET
        else:
            worker_selector = (
                PaginatedResponseActionSummaryItemsItemWorkerSelector.from_dict(
                    _worker_selector
                )
            )

        _worker_tolerations = d.pop("worker_tolerations", UNSET)
        worker_tolerations: list[WorkerToleration] | Unset = UNSET
        if _worker_tolerations is not UNSET:
            worker_tolerations = []
            for worker_tolerations_item_data in _worker_tolerations:
                worker_tolerations_item = WorkerToleration.from_dict(
                    worker_tolerations_item_data
                )

                worker_tolerations.append(worker_tolerations_item)

        def _parse_workflow_def(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        workflow_def = _parse_workflow_def(d.pop("workflow_def", UNSET))

        paginated_response_action_summary_items_item = cls(
            accesses_mcp=accesses_mcp,
            created=created,
            entrypoint=entrypoint,
            id=id,
            label=label,
            pack_ref=pack_ref,
            ref=ref,
            updated=updated,
            artifact_retention_limit=artifact_retention_limit,
            artifact_retention_policy=artifact_retention_policy,
            default_execution_permission_set_refs=default_execution_permission_set_refs,
            description=description,
            log_retention_limit=log_retention_limit,
            log_retention_policy=log_retention_policy,
            required_worker_runtimes=required_worker_runtimes,
            runtime=runtime,
            runtime_ref=runtime_ref,
            runtime_version_constraint=runtime_version_constraint,
            worker_affinity=worker_affinity,
            worker_selector=worker_selector,
            worker_tolerations=worker_tolerations,
            workflow_def=workflow_def,
        )

        paginated_response_action_summary_items_item.additional_properties = d
        return paginated_response_action_summary_items_item

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

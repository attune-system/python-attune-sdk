import hashlib
import importlib
import json
import os
from http import HTTPStatus
from pathlib import Path

import httpx

from attune.api_client import AuthenticatedClient
from attune.api_client.api.events import create_event
from attune.api_client.api.executions import list_workflow_cache_iterations
from attune.api_client.api.queues import bulk_enqueue_queue_items
from attune.api_client.api.secrets import get_key
from attune.api_client.models.bulk_enqueue_work_queue_items_request import (
    BulkEnqueueWorkQueueItemsRequest,
)
from attune.api_client.models.create_event_request import CreateEventRequest
from attune.api_client.models.create_event_request_config_type_0 import (
    CreateEventRequestConfigType0,
)
from attune.api_client.models.create_event_request_payload_type_0 import (
    CreateEventRequestPayloadType0,
)
from attune.api_client.models.enqueue_work_queue_item_request import (
    EnqueueWorkQueueItemRequest,
)
from attune.api_client.models.enqueue_work_queue_item_request_payload import (
    EnqueueWorkQueueItemRequestPayload,
)
from attune.api_client.models.install_pack_request import InstallPackRequest
from attune.api_client.models.save_workflow_file_request import SaveWorkflowFileRequest
from attune.api_client.models.save_workflow_file_request_definition import (
    SaveWorkflowFileRequestDefinition,
)
from attune.api_client.models.save_workflow_file_request_out_schema_type_0 import (
    SaveWorkflowFileRequestOutSchemaType0,
)
from attune.api_client.models.save_workflow_file_request_param_schema_type_0 import (
    SaveWorkflowFileRequestParamSchemaType0,
)

API_DIR = Path(__file__).parents[1] / "src" / "attune" / "api_client" / "api"
HTTP_METHODS = {"delete", "get", "head", "options", "patch", "post", "put", "trace"}


def test_create_event_posts_optional_payload():
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["content"] = request.content
        return httpx.Response(400, request=request)

    payload = CreateEventRequestPayloadType0()
    payload["ticket_id"] = "INC-123"
    body = CreateEventRequest(
        trigger_ref="my_pack.follow_up_requested",
        payload=payload,
    )

    with httpx.Client(
        base_url="https://attune.test",
        transport=httpx.MockTransport(handler),
    ) as http_client:
        client = AuthenticatedClient(
            base_url="https://attune.test",
            token="test-token",
        ).set_httpx_client(http_client)
        response = create_event.sync_detailed(client=client, body=body)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.parsed is None
    assert captured["method"] == "POST"
    assert captured["path"] == "/api/v1/events"
    assert json.loads(captured["content"]) == {
        "payload": {"ticket_id": "INC-123"},
        "trigger_ref": "my_pack.follow_up_requested",
    }


def test_create_event_nullable_payload_and_config_contract():
    omitted = CreateEventRequest(trigger_ref="core.timer").to_dict()
    assert "payload" not in omitted
    assert "config" not in omitted

    nullable = CreateEventRequest.from_dict(
        {"trigger_ref": "core.timer", "payload": None, "config": None}
    )
    assert nullable.to_dict() == {
        "trigger_ref": "core.timer",
        "payload": None,
        "config": None,
    }

    payload = CreateEventRequestPayloadType0.from_dict({"count": 3})
    config = CreateEventRequestConfigType0.from_dict({"source": "test"})
    assert CreateEventRequest(
        trigger_ref="core.timer", payload=payload, config=config
    ).to_dict() == {
        "trigger_ref": "core.timer",
        "payload": {"count": 3},
        "config": {"source": "test"},
    }


def test_get_key_sends_decrypt_only_when_explicit():
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(404, request=request)

    with httpx.Client(
        base_url="https://attune.test", transport=httpx.MockTransport(handler)
    ) as http_client:
        client = AuthenticatedClient(
            base_url="https://attune.test", token="test-token"
        ).set_httpx_client(http_client)
        get_key.sync_detailed("secret.value", client=client)
        get_key.sync_detailed("secret.value", client=client, decrypt=True)

    assert requests[0].url.path == "/api/v1/keys/secret.value"
    assert requests[0].url.query == b""
    assert dict(requests[1].url.params) == {"decrypt": "true"}


def test_install_pack_no_registry_contract():
    assert InstallPackRequest(source="https://example.test/pack.git").to_dict() == {
        "source": "https://example.test/pack.git"
    }
    assert InstallPackRequest(
        source="https://example.test/pack.git", no_registry=False
    ).to_dict()["no_registry"] is False
    assert InstallPackRequest(
        source="https://example.test/pack.git", no_registry=True
    ).to_dict()["no_registry"] is True


def test_save_workflow_file_omission_vs_explicit_empty_contract():
    required = {
        "definition": SaveWorkflowFileRequestDefinition(),
        "label": "Example",
        "name": "example",
        "pack_ref": "core",
        "version": "1.0.0",
    }

    omitted = SaveWorkflowFileRequest(**required).to_dict()
    assert "param_schema" not in omitted
    assert "out_schema" not in omitted
    assert "tags" not in omitted
    assert "reference_allowed_pack_refs" not in omitted

    explicit_empty = SaveWorkflowFileRequest(
        **required,
        param_schema=SaveWorkflowFileRequestParamSchemaType0(),
        out_schema=SaveWorkflowFileRequestOutSchemaType0(),
        tags=[],
        reference_allowed_pack_refs=[],
    ).to_dict()
    assert explicit_empty["param_schema"] == {}
    assert explicit_empty["out_schema"] == {}
    assert explicit_empty["tags"] == []
    assert explicit_empty["reference_allowed_pack_refs"] == []


def test_cache_operations_are_present():
    expected = {
        "abandon_generation",
        "create_generation",
        "create_namespace",
        "delete_namespace",
        "list_generations",
        "list_namespaces",
        "lookup_entries",
        "lookup_entry",
        "promote_generation",
        "scan_entries",
        "seal_generation",
        "show_generation",
        "show_namespace",
        "update_namespace",
        "upload_chunk",
    }
    generated = {path.stem for path in (API_DIR / "caches").glob("*.py")} - {
        "__init__"
    }
    assert generated == expected
    for operation in expected:
        importlib.import_module(f"attune.api_client.api.caches.{operation}")


def test_list_workflow_cache_iterations_contract():
    captured: dict[str, object] = {}
    response_body = {
        "data": [
            {
                "batch_size": 10,
                "concurrency": 2,
                "created": "2026-08-11T12:00:00Z",
                "dispatched_count": 7,
                "generation_id": 22,
                "namespace_id": 11,
                "page_size": 100,
                "scanned_count": 10,
                "state": "scanning",
                "task_name": "fan_out",
                "updated": "2026-08-11T12:01:00Z",
            }
        ]
    }

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        return httpx.Response(200, json=response_body, request=request)

    with httpx.Client(
        base_url="https://attune.test", transport=httpx.MockTransport(handler)
    ) as http_client:
        client = AuthenticatedClient(
            base_url="https://attune.test", token="test-token"
        ).set_httpx_client(http_client)
        response = list_workflow_cache_iterations.sync_detailed(42, client=client)

    assert captured == {
        "method": "GET",
        "path": "/api/v1/executions/42/workflow-cache-iterations",
    }
    assert response.status_code == HTTPStatus.OK
    assert response.parsed is not None
    assert len(response.parsed.data) == 1
    iteration = response.parsed.data[0]
    assert iteration.task_name == "fan_out"
    assert iteration.state.value == "scanning"
    assert iteration.generation_id == 22


def test_generated_operation_inventory_matches_openapi_or_checked_snapshot():
    generated = sorted(
        str(path.relative_to(API_DIR).with_suffix(""))
        for path in API_DIR.glob("*/*.py")
        if path.name != "__init__.py"
    )
    spec_path = os.environ.get("ATTUNE_OPENAPI_PATH")
    if spec_path:
        with Path(spec_path).open(encoding="utf-8") as spec_file:
            spec = json.load(spec_file)
        expected = sorted(
            f'{operation["tags"][0]}/{operation["operationId"]}'
            for path_item in spec["paths"].values()
            for method, operation in path_item.items()
            if method.lower() in HTTP_METHODS
        )
        assert generated == expected
        return

    fixture_path = Path(__file__).with_name("openapi-operation-inventory.json")
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    digest = hashlib.sha256("\n".join(generated).encode()).hexdigest()
    assert len(generated) == fixture["operation_count"]
    assert digest == fixture["sha256"]


def test_bulk_enqueue_posts_items():
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["content"] = request.content
        return httpx.Response(400, request=request)

    payload = EnqueueWorkQueueItemRequestPayload()
    payload["order_id"] = 123
    body = BulkEnqueueWorkQueueItemsRequest(
        items=[
            EnqueueWorkQueueItemRequest(
                item_key="order-123",
                payload=payload,
                priority=5,
            )
        ]
    )

    with httpx.Client(
        base_url="https://attune.test",
        transport=httpx.MockTransport(handler),
    ) as http_client:
        client = AuthenticatedClient(
            base_url="https://attune.test",
            token="test-token",
        ).set_httpx_client(http_client)
        response = bulk_enqueue_queue_items.sync_detailed(
            "core.inbox",
            client=client,
            body=body,
        )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.parsed is None
    assert captured["method"] == "POST"
    assert captured["path"] == "/api/v1/queues/core.inbox/items/bulk"
    assert json.loads(captured["content"]) == {
        "items": [
            {
                "item_key": "order-123",
                "payload": {"order_id": 123},
                "priority": 5,
            }
        ]
    }

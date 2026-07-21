import json
from http import HTTPStatus

import httpx

from attune.api_client import AuthenticatedClient
from attune.api_client.api.events import create_event
from attune.api_client.api.queues import bulk_enqueue_queue_items
from attune.api_client.models.bulk_enqueue_work_queue_items_request import (
    BulkEnqueueWorkQueueItemsRequest,
)
from attune.api_client.models.create_event_request import CreateEventRequest
from attune.api_client.models.create_event_request_payload import (
    CreateEventRequestPayload,
)
from attune.api_client.models.enqueue_work_queue_item_request import (
    EnqueueWorkQueueItemRequest,
)
from attune.api_client.models.enqueue_work_queue_item_request_payload import (
    EnqueueWorkQueueItemRequestPayload,
)


def test_create_event_posts_optional_payload():
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["content"] = request.content
        return httpx.Response(400, request=request)

    payload = CreateEventRequestPayload()
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

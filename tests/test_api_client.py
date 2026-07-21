import json
from http import HTTPStatus

import httpx

from attune.api_client import AuthenticatedClient
from attune.api_client.api.events import create_event
from attune.api_client.models.create_event_request import CreateEventRequest
from attune.api_client.models.create_event_request_payload import (
    CreateEventRequestPayload,
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

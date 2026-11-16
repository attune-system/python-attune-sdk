from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_response_webhook_management_response import (
    ApiResponseWebhookManagementResponse,
)
from ...types import Response


def _get_kwargs(
    ref: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/triggers/{ref}/webhooks/reveal".format(
            ref=quote(str(ref), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiResponseWebhookManagementResponse | None:
    if response.status_code == 200:
        response_200 = ApiResponseWebhookManagementResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ApiResponseWebhookManagementResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ref: str,
    *,
    client: AuthenticatedClient,
) -> Response[ApiResponseWebhookManagementResponse]:
    """Explicitly reveal the webhook bearer credential to an authorized manager.

    Args:
        ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResponseWebhookManagementResponse]
    """

    kwargs = _get_kwargs(
        ref=ref,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ref: str,
    *,
    client: AuthenticatedClient,
) -> ApiResponseWebhookManagementResponse | None:
    """Explicitly reveal the webhook bearer credential to an authorized manager.

    Args:
        ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResponseWebhookManagementResponse
    """

    return sync_detailed(
        ref=ref,
        client=client,
    ).parsed


async def asyncio_detailed(
    ref: str,
    *,
    client: AuthenticatedClient,
) -> Response[ApiResponseWebhookManagementResponse]:
    """Explicitly reveal the webhook bearer credential to an authorized manager.

    Args:
        ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResponseWebhookManagementResponse]
    """

    kwargs = _get_kwargs(
        ref=ref,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ref: str,
    *,
    client: AuthenticatedClient,
) -> ApiResponseWebhookManagementResponse | None:
    """Explicitly reveal the webhook bearer credential to an authorized manager.

    Args:
        ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResponseWebhookManagementResponse
    """

    return (
        await asyncio_detailed(
            ref=ref,
            client=client,
        )
    ).parsed

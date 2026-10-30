from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sensor_runtime_revocation_request import SensorRuntimeRevocationRequest
from ...models.success_response import SuccessResponse
from ...types import Response


def _get_kwargs(
    ref: str,
    *,
    body: SensorRuntimeRevocationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/sensors/{ref}/revoke-runtime".format(
            ref=quote(str(ref), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SuccessResponse | None:
    if response.status_code == 200:
        response_200 = SuccessResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SuccessResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ref: str,
    *,
    client: AuthenticatedClient | Client,
    body: SensorRuntimeRevocationRequest,
) -> Response[SuccessResponse]:
    """
    Args:
        ref (str):
        body (SensorRuntimeRevocationRequest): Explicit operational revocation, separate from
            disablement or human IAM edits.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SuccessResponse]
    """

    kwargs = _get_kwargs(
        ref=ref,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ref: str,
    *,
    client: AuthenticatedClient | Client,
    body: SensorRuntimeRevocationRequest,
) -> SuccessResponse | None:
    """
    Args:
        ref (str):
        body (SensorRuntimeRevocationRequest): Explicit operational revocation, separate from
            disablement or human IAM edits.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SuccessResponse
    """

    return sync_detailed(
        ref=ref,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    ref: str,
    *,
    client: AuthenticatedClient | Client,
    body: SensorRuntimeRevocationRequest,
) -> Response[SuccessResponse]:
    """
    Args:
        ref (str):
        body (SensorRuntimeRevocationRequest): Explicit operational revocation, separate from
            disablement or human IAM edits.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SuccessResponse]
    """

    kwargs = _get_kwargs(
        ref=ref,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ref: str,
    *,
    client: AuthenticatedClient | Client,
    body: SensorRuntimeRevocationRequest,
) -> SuccessResponse | None:
    """
    Args:
        ref (str):
        body (SensorRuntimeRevocationRequest): Explicit operational revocation, separate from
            disablement or human IAM edits.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SuccessResponse
    """

    return (
        await asyncio_detailed(
            ref=ref,
            client=client,
            body=body,
        )
    ).parsed

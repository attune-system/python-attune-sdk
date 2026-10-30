from http import HTTPStatus
from io import BytesIO
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import File, Response


def _get_kwargs(
    pack_ref: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/internal/packs/{pack_ref}/archive".format(
            pack_ref=quote(str(pack_ref), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | File | None:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

        return response_200

    if response.status_code == 206:
        response_206 = File(payload=BytesIO(response.content))

        return response_206

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 416:
        response_416 = cast(Any, None)
        return response_416

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pack_ref: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | File]:
    """Return the deterministic archive for a pack's active release.

     Used by remote workers/sensors to download pack contents when they
    don't share a mounted volume with the API.

    Args:
        pack_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | File]
    """

    kwargs = _get_kwargs(
        pack_ref=pack_ref,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pack_ref: str,
    *,
    client: AuthenticatedClient,
) -> Any | File | None:
    """Return the deterministic archive for a pack's active release.

     Used by remote workers/sensors to download pack contents when they
    don't share a mounted volume with the API.

    Args:
        pack_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | File
    """

    return sync_detailed(
        pack_ref=pack_ref,
        client=client,
    ).parsed


async def asyncio_detailed(
    pack_ref: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | File]:
    """Return the deterministic archive for a pack's active release.

     Used by remote workers/sensors to download pack contents when they
    don't share a mounted volume with the API.

    Args:
        pack_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | File]
    """

    kwargs = _get_kwargs(
        pack_ref=pack_ref,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pack_ref: str,
    *,
    client: AuthenticatedClient,
) -> Any | File | None:
    """Return the deterministic archive for a pack's active release.

     Used by remote workers/sensors to download pack contents when they
    don't share a mounted volume with the API.

    Args:
        pack_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | File
    """

    return (
        await asyncio_detailed(
            pack_ref=pack_ref,
            client=client,
        )
    ).parsed

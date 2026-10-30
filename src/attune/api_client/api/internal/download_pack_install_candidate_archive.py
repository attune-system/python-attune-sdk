from http import HTTPStatus
from io import BytesIO
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import File, Response


def _get_kwargs(
    pack_install_id: int,
    *,
    x_attune_pack_candidate_token: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["x-attune-pack-candidate-token"] = x_attune_pack_candidate_token

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/internal/pack-installs/{pack_install_id}/archive".format(
            pack_install_id=quote(str(pack_install_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | File | None:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

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
    pack_install_id: int,
    *,
    client: AuthenticatedClient,
    x_attune_pack_candidate_token: str,
) -> Response[Any | File]:
    """Stream the version-pinned candidate object for an assigned pack-install test.

    Args:
        pack_install_id (int):
        x_attune_pack_candidate_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | File]
    """

    kwargs = _get_kwargs(
        pack_install_id=pack_install_id,
        x_attune_pack_candidate_token=x_attune_pack_candidate_token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pack_install_id: int,
    *,
    client: AuthenticatedClient,
    x_attune_pack_candidate_token: str,
) -> Any | File | None:
    """Stream the version-pinned candidate object for an assigned pack-install test.

    Args:
        pack_install_id (int):
        x_attune_pack_candidate_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | File
    """

    return sync_detailed(
        pack_install_id=pack_install_id,
        client=client,
        x_attune_pack_candidate_token=x_attune_pack_candidate_token,
    ).parsed


async def asyncio_detailed(
    pack_install_id: int,
    *,
    client: AuthenticatedClient,
    x_attune_pack_candidate_token: str,
) -> Response[Any | File]:
    """Stream the version-pinned candidate object for an assigned pack-install test.

    Args:
        pack_install_id (int):
        x_attune_pack_candidate_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | File]
    """

    kwargs = _get_kwargs(
        pack_install_id=pack_install_id,
        x_attune_pack_candidate_token=x_attune_pack_candidate_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pack_install_id: int,
    *,
    client: AuthenticatedClient,
    x_attune_pack_candidate_token: str,
) -> Any | File | None:
    """Stream the version-pinned candidate object for an assigned pack-install test.

    Args:
        pack_install_id (int):
        x_attune_pack_candidate_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | File
    """

    return (
        await asyncio_detailed(
            pack_install_id=pack_install_id,
            client=client,
            x_attune_pack_candidate_token=x_attune_pack_candidate_token,
        )
    ).parsed

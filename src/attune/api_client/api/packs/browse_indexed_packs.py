from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.browse_indexed_packs_response_200 import BrowseIndexedPacksResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str | Unset = UNSET,
    registry_id: int | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    params["registry_id"] = registry_id

    params["include_disabled"] = include_disabled

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/pack-indices/packs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | BrowseIndexedPacksResponse200 | None:
    if response.status_code == 200:
        response_200 = BrowseIndexedPacksResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | BrowseIndexedPacksResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    q: str | Unset = UNSET,
    registry_id: int | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> Response[Any | BrowseIndexedPacksResponse200]:
    """
    Args:
        q (str | Unset):
        registry_id (int | Unset):
        include_disabled (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BrowseIndexedPacksResponse200]
    """

    kwargs = _get_kwargs(
        q=q,
        registry_id=registry_id,
        include_disabled=include_disabled,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    q: str | Unset = UNSET,
    registry_id: int | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> Any | BrowseIndexedPacksResponse200 | None:
    """
    Args:
        q (str | Unset):
        registry_id (int | Unset):
        include_disabled (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BrowseIndexedPacksResponse200
    """

    return sync_detailed(
        client=client,
        q=q,
        registry_id=registry_id,
        include_disabled=include_disabled,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    q: str | Unset = UNSET,
    registry_id: int | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> Response[Any | BrowseIndexedPacksResponse200]:
    """
    Args:
        q (str | Unset):
        registry_id (int | Unset):
        include_disabled (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BrowseIndexedPacksResponse200]
    """

    kwargs = _get_kwargs(
        q=q,
        registry_id=registry_id,
        include_disabled=include_disabled,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    q: str | Unset = UNSET,
    registry_id: int | Unset = UNSET,
    include_disabled: bool | Unset = UNSET,
) -> Any | BrowseIndexedPacksResponse200 | None:
    """
    Args:
        q (str | Unset):
        registry_id (int | Unset):
        include_disabled (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BrowseIndexedPacksResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            registry_id=registry_id,
            include_disabled=include_disabled,
        )
    ).parsed

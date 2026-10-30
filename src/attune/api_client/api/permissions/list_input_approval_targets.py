from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.paginated_response_declared_input_approval_target import (
    PaginatedResponseDeclaredInputApprovalTarget,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    pack_ref: str,
    *,
    policy_revision: int | None | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_policy_revision: int | None | Unset
    if isinstance(policy_revision, Unset):
        json_policy_revision = UNSET
    else:
        json_policy_revision = policy_revision
    params["policy_revision"] = json_policy_revision

    params["page"] = page

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/packs/{pack_ref}/input-approval-targets".format(
            pack_ref=quote(str(pack_ref), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PaginatedResponseDeclaredInputApprovalTarget | None:
    if response.status_code == 200:
        response_200 = PaginatedResponseDeclaredInputApprovalTarget.from_dict(
            response.json()
        )

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PaginatedResponseDeclaredInputApprovalTarget]:
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
    policy_revision: int | None | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
) -> Response[PaginatedResponseDeclaredInputApprovalTarget]:
    """
    Args:
        pack_ref (str):
        policy_revision (int | None | Unset):
        page (int | Unset):
        page_size (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedResponseDeclaredInputApprovalTarget]
    """

    kwargs = _get_kwargs(
        pack_ref=pack_ref,
        policy_revision=policy_revision,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pack_ref: str,
    *,
    client: AuthenticatedClient,
    policy_revision: int | None | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
) -> PaginatedResponseDeclaredInputApprovalTarget | None:
    """
    Args:
        pack_ref (str):
        policy_revision (int | None | Unset):
        page (int | Unset):
        page_size (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedResponseDeclaredInputApprovalTarget
    """

    return sync_detailed(
        pack_ref=pack_ref,
        client=client,
        policy_revision=policy_revision,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    pack_ref: str,
    *,
    client: AuthenticatedClient,
    policy_revision: int | None | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
) -> Response[PaginatedResponseDeclaredInputApprovalTarget]:
    """
    Args:
        pack_ref (str):
        policy_revision (int | None | Unset):
        page (int | Unset):
        page_size (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedResponseDeclaredInputApprovalTarget]
    """

    kwargs = _get_kwargs(
        pack_ref=pack_ref,
        policy_revision=policy_revision,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pack_ref: str,
    *,
    client: AuthenticatedClient,
    policy_revision: int | None | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
) -> PaginatedResponseDeclaredInputApprovalTarget | None:
    """
    Args:
        pack_ref (str):
        policy_revision (int | None | Unset):
        page (int | Unset):
        page_size (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedResponseDeclaredInputApprovalTarget
    """

    return (
        await asyncio_detailed(
            pack_ref=pack_ref,
            client=client,
            policy_revision=policy_revision,
            page=page,
            page_size=page_size,
        )
    ).parsed

"""
Lightweight HTTP client for the Attune API.

Uses the execution-scoped API token from the environment. Built on top of
the generated OpenAPI client (``attune.api_client``).

Usage::

    from attune.client import AttuneClient

    client = AttuneClient()  # auto-reads ATTUNE_API_URL and ATTUNE_API_TOKEN
    artifacts = client.get("/api/v1/artifacts", params={"execution": 42})

For full typed access to every API endpoint, use the generated client directly::

    from attune.api_client import AuthenticatedClient
    from attune.api_client.api.packs import list_packs

    client = AuthenticatedClient(base_url="http://localhost:8080", token="...")
    response = list_packs.sync(client=client)
"""

from __future__ import annotations

import os
from typing import Any

from attune.api_client import AuthenticatedClient, Client


class AttuneClient:
    """Minimal HTTP client for the Attune REST API.

    Reads ``ATTUNE_API_URL`` and ``ATTUNE_API_TOKEN`` from the environment
    by default.

    For typed, endpoint-specific calls, access ``.api_client`` which is an
    instance of the generated ``AuthenticatedClient`` (or ``Client`` if no
    token is available).
    """

    def __init__(
        self,
        *,
        api_url: str | None = None,
        api_token: str | None = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
    ) -> None:
        self.api_url = (
            api_url or os.environ.get("ATTUNE_API_URL") or "http://localhost:8080"
        ).rstrip("/")
        self.api_token = api_token or os.environ.get("ATTUNE_API_TOKEN") or ""
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self._api_client: AuthenticatedClient | Client | None = None

    @property
    def api_client(self) -> AuthenticatedClient | Client:
        """The underlying generated API client instance."""
        if self._api_client is None:
            import httpx

            timeout = httpx.Timeout(self.timeout)
            if self.api_token:
                self._api_client = AuthenticatedClient(
                    base_url=self.api_url,
                    token=self.api_token,
                    timeout=timeout,
                    verify_ssl=self.verify_ssl,
                )
            else:
                self._api_client = Client(
                    base_url=self.api_url,
                    timeout=timeout,
                    verify_ssl=self.verify_ssl,
                )
        return self._api_client

    @property
    def _httpx(self) -> Any:
        """Lazy-initialized httpx.Client for raw requests."""
        return self.api_client.get_httpx_client()

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        """Send a GET request and return the JSON response body."""
        resp = self._httpx.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    def post(self, path: str, *, json: Any = None) -> Any:
        """Send a POST request and return the JSON response body."""
        resp = self._httpx.post(path, json=json)
        resp.raise_for_status()
        return resp.json()

    def put(self, path: str, *, json: Any = None) -> Any:
        """Send a PUT request and return the JSON response body."""
        resp = self._httpx.put(path, json=json)
        resp.raise_for_status()
        return resp.json()

    def delete(self, path: str) -> Any:
        """Send a DELETE request and return the JSON response body."""
        resp = self._httpx.delete(path)
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return None

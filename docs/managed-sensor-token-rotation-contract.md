# Managed Sensor Token Rotation (Python SDK)

This document describes Python SDK token consumption and the current managed
sensor runtime process.

## 1) Security model (normative)

- **Rotation is runtime/platform driven**. The current managed sensor service
  provisions a replacement token and performs a controlled process restart.
- SDKs **must not** implement self-refresh flows that depend on using an expired token.
- SDKs consume externally rotated state and reconnect/retry with the latest state.

## 2) Token state sources and precedence

### Python source precedence
1. `ATTUNE_SENSOR_TOKEN_STATE_PATH` JSON file (runtime-managed, read on demand)
2. Fallback token env (`ATTUNE_API_TOKEN` + optional expiry metadata)

The current managed service injects `ATTUNE_API_TOKEN` and does not inject a
token-state path. `ATTUNE_SENSOR_TOKEN_STATE_PATH` is available for external
runtimes that implement atomic file replacement.

## 3) Token state JSON shape

### Canonical shape (recommended)

```json
{
  "token": "eyJ...",
  "expires_at": "2026-12-31T00:00:00Z"
}
```

### Compatibility aliases

- Token alias: `api_token`
- Expiry alias: `token_expires_at`

## 4) Expiry metadata expectations

- `expires_at` should be RFC3339/ISO-8601 UTC (for example `2026-12-31T00:00:00Z`).
- Supplying expiry metadata is strongly recommended so reconnect logic can rotate before server-side token expiry.
- If expiry metadata is missing, SDKs continue using token value rotation but cannot pre-schedule expiry-based reconnects.

## 5) Notifier reconnect behavior

- The Python SDK reconnects notifier WebSocket connections in a loop and
  re-resolves token state on new connects.
- If the notifier closes a connection due to expiry (for example close code `4401`), reconnect must use latest rotated token state.

- Python reconnects when token state changes or when a file-provided token is
  expiring within `ATTUNE_SENSOR_TOKEN_RECONNECT_WINDOW_SECONDS` (default `30`).
- For the current managed service, token replacement is delivered by process
  restart rather than an in-process reconnect.

## 6) Backward-compat and local-dev fallback

- If no token-state file is configured, SDKs can run with `ATTUNE_API_TOKEN` for local development.
- If token-state file reads fail, Python uses the fallback environment token
  when available; otherwise it raises a clear token-source error.

## 7) Safe failure semantics

- No SDK should attempt self-refresh with expired credentials.
- Missing/invalid token state must result in explicit auth failure behavior (clear errors and/or reconnect retries), not silent token fabrication.
- Sensor authors should always read token state through SDK accessors (`current_api_token` / `getApiToken()` / `apiToken()`) instead of caching startup token values.

## 8) Runtime/platform writer requirements

Runtime/platform code that rotates managed sensor tokens should:

1. Keep `ATTUNE_SENSOR_TOKEN_STATE_PATH` stable.
2. Write valid JSON objects with at least `token` (and preferably `expires_at`).
3. Use atomic file replacement semantics to avoid partial-read JSON corruption.
4. Rotate before expiry with enough lead time for reconnect windows (~30s default across SDKs).

## 9) Conformance test coverage

Python coverage lives in `tests/test_context.py` and `tests/test_sensor.py`.

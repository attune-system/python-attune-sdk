# attune — Python SDK for Attune Actions & Sensors

A lightweight Python package providing boilerplate for writing [Attune](https://github.com/attune-system/attune) actions and sensors.

SDK 0.4.0 is generated from the Attune OpenAPI 0.4.2 contract.

## Installation

```bash
pip install attune-sdk              # includes API client, httpx, attrs
pip install attune-sdk[sensor]      # adds websocket-client for managed sensors
pip install attune-sdk[dev]         # adds pytest + openapi-python-client
```

## Writing Actions

Actions receive parameters as JSON on stdin and output results as JSON on stdout.
This package handles all of that:

```python
#!/usr/bin/env python3
import attune

def main(name: str, count: int = 1):
    return {"greeting": f"Hello, {name}!" * count}

attune.run_action(main)
```

Your function declares whatever parameters it needs as keyword arguments —
they're matched from the JSON input. Extra parameters not in your signature
are silently dropped (unless you add `**kwargs`).

### Accessing Execution Context

The context is a module-level singleton available anywhere after import:

```python
import attune

def main(url: str, method: str = "GET"):
    if attune.context.has_api_token:
        from attune.api_client.api.packs import list_packs
        packs = list_packs.sync(client=attune.context.client)
        # ...
    return {"action": attune.context.action_ref, "exec_id": attune.context.execution_id}

attune.run_action(main)
```

### Working with Artifacts

Use `attune.artifacts` for action-owned artifacts with context-aware defaults.
The helpers default `scope="action"`, `owner=attune.context.action_ref`,
`created_by=attune.context.action_ref`, `execution=attune.context.execution_id`
(when present), and `visibility="private"`.

```python
import attune

def main():
    allocation = attune.artifacts.allocate_file_version(
        "python_example.demo.log",
        name="Execution Log",
    )
    allocation.write_text("hello\n")

    progress = attune.artifacts.create_progress("python_example.demo.progress")
    progress.append({"message": "started", "percent": 10})

    return {
        "artifact_id": allocation.artifact_id,
        "version_id": allocation.version_id,
        "file_path": allocation.file_path,
        "path": str(allocation.absolute_path),
    }

attune.run_action(main)
```

`allocate_file_version()` uses Attune's upsert-and-allocate API, returns the
local absolute path under `ATTUNE_ARTIFACTS_DIR`, and creates parent
directories for you. `create_progress()` creates or reuses a progress artifact
and `append()` streams entries without silent failure paths.

### Using the API Client

The SDK includes a fully typed, auto-generated OpenAPI client. The easiest way
to use it is via `attune.context.client` which is a lazily constructed
`AuthenticatedClient` using the execution-scoped token:

```python
import attune
from attune.api_client.api.packs import list_packs
from attune.api_client.api.executions import get_execution

# Sync — use endpoint_name.sync(client=...)
packs = list_packs.sync(client=attune.context.client)
if packs is None:
    raise RuntimeError("Unable to list packs")
pack_data = packs.to_dict()

# Async — use endpoint_name.asyncio(client=...) with the same client instance
packs = await list_packs.asyncio(client=attune.context.client)
```

The same client instance handles both sync and async calls — no separate
async client needed. Each endpoint module exposes four functions:

| Function | Returns |
|----------|---------|
| `sync(client=...)` | Parsed response model (or `None`) |
| `sync_detailed(client=...)` | `Response[T]` with status, headers, content |
| `asyncio(client=...)` | Parsed response model (async) |
| `asyncio_detailed(client=...)` | `Response[T]` (async) |

Generated endpoint helpers may return `None` for documented error responses.
Check the result before accessing fields. Generated response and model objects
provide `to_dict()` when a plain JSON-compatible dictionary is needed.

**Constructing a client manually** (e.g., outside an execution):

```python
from attune.api_client import AuthenticatedClient
client = AuthenticatedClient(base_url="http://localhost:8080", token="your-token")
```

All API modules live under `attune.api_client.api.<domain>` and all request/response
models under `attune.api_client.models`.

#### Create and Read a Key

Create keys with a `local_ref` and a textual owner reference. The server returns
the canonical `ref`; use that returned value for get, update, and delete calls.

```python
import attune
from attune.api_client.api.secrets import create_key, get_key
from attune.api_client.models.create_key_request import CreateKeyRequest
from attune.api_client.models.owner_type import OwnerType

created = create_key.sync(
    client=attune.context.client,
    body=CreateKeyRequest(
        local_ref="github_token",
        name="GitHub API Token",
        owner_type=OwnerType.PACK,
        owner_pack_ref="github",
        value="replace-with-secret-value",
        encrypted=True,
    ),
)
if created is None:
    raise RuntimeError("Unable to create key")

canonical_ref = created.data.ref  # e.g. "pack.github.github_token"
key = get_key.sync(canonical_ref, client=attune.context.client)
```

Do not reconstruct the canonical ref from `local_ref`, and do not pass a local
ref to `get_key`, `update_key`, or `delete_key`.

### Common Action Tasks

Actions can use the typed API client with their execution-scoped credentials for
common platform operations.

#### Enqueue One Item

```python
import attune
from attune.api_client.api.queues import enqueue_queue_item
from attune.api_client.models.enqueue_work_queue_item_request import EnqueueWorkQueueItemRequest
from attune.api_client.models.enqueue_work_queue_item_request_payload import (
    EnqueueWorkQueueItemRequestPayload,
)

def main(order_id: str):
    enqueue_queue_item.sync(
        "acme.orders",
        client=attune.context.client,
        body=EnqueueWorkQueueItemRequest(
            item_key=f"order-{order_id}",
            priority=10,
            payload=EnqueueWorkQueueItemRequestPayload.from_dict(
                {"order_id": order_id}
            ),
        ),
    )
    return {"queued_order_id": order_id}

attune.run_action(main)
```

#### Enqueue a Batch

Use the bulk endpoint to enqueue all items in one request. Give each item a
stable key so it can be identified across submissions:

```python
import attune
from attune.api_client.api.queues import bulk_enqueue_queue_items
from attune.api_client.models.bulk_enqueue_work_queue_items_request import (
    BulkEnqueueWorkQueueItemsRequest,
)
from attune.api_client.models.enqueue_work_queue_item_request import EnqueueWorkQueueItemRequest
from attune.api_client.models.enqueue_work_queue_item_request_payload import (
    EnqueueWorkQueueItemRequestPayload,
)

def main(order_ids: list[str]):
    result = bulk_enqueue_queue_items.sync(
        "acme.orders",
        client=attune.context.client,
        body=BulkEnqueueWorkQueueItemsRequest(
            items=[
                EnqueueWorkQueueItemRequest(
                    item_key=f"order-{order_id}",
                    payload=EnqueueWorkQueueItemRequestPayload.from_dict(
                        {"order_id": order_id}
                    ),
                )
                for order_id in order_ids
            ],
        )
    )
    if result is None:
        raise RuntimeError("Bulk queue enqueue failed")
    return {
        "created_count": result.data.created_count,
        "updated_count": result.data.updated_count,
    }

attune.run_action(main)
```

#### Emit an Event

```python
import attune
from attune.api_client.api.events import create_event
from attune.api_client.models.create_event_request import CreateEventRequest
from attune.api_client.models.create_event_request_payload_type_0 import (
    CreateEventRequestPayloadType0,
)

def main(deployment_id: str, environment: str):
    create_event.sync(
        client=attune.context.client,
        body=CreateEventRequest(
            trigger_ref="acme.deployment.completed",
            payload=CreateEventRequestPayloadType0.from_dict(
                {"deployment_id": deployment_id, "environment": environment}
            ),
        ),
    )
    return {"emitted_event": "acme.deployment.completed"}

attune.run_action(main)
```

#### Read a File Artifact

Pass the `file_path` returned by `allocate_file_version()` to a downstream
action. It is relative to the shared artifact volume, so resolve and validate
it before reading:

```python
import attune

def main(file_path: str):
    artifacts_dir = attune.context.artifacts_dir
    if artifacts_dir is None:
        raise RuntimeError("ATTUNE_ARTIFACTS_DIR is required to read file artifacts")

    root = artifacts_dir.resolve()
    artifact_path = (root / file_path).resolve()
    if not artifact_path.is_relative_to(root):
        raise ValueError("file_path must remain within ATTUNE_ARTIFACTS_DIR")

    return {"contents": artifact_path.read_text(encoding="utf-8")}

attune.run_action(main)
```

## Writing Sensors

Sensors are long-running processes that emit events. The SDK provides rule
lifecycle management, signal handling (SIGINT/SIGTERM), and notifier WebSocket lifecycle delivery out of the box.

The sensor context is a module-level singleton, accessible anywhere:

```python
import attune

# attune.sensor_context is available at import time
print(attune.sensor_context.sensor_ref)
print(attune.sensor_context.api_url)
print(attune.sensor_context.config)  # caller-supplied ATTUNE_SENSOR_CONFIG_* vars
```

The current managed sensor service rotates credentials with a controlled
process restart and injects the replacement `ATTUNE_API_TOKEN` into the new
process. The SDK also supports an externally managed token-state file for
nonstandard runtimes; see
[docs/managed-sensor-token-rotation-contract.md](docs/managed-sensor-token-rotation-contract.md).

Persisted sensor `config` is not injected into managed child processes.
Use each rule's `trigger_params` for managed configuration, or retrieve other
configuration from an explicitly authorized source. `sensor_context.config`
only exposes `ATTUNE_SENSOR_CONFIG_*` variables supplied by the caller.

### Synchronous Polling (`PollingSensor`)

One polling thread per active rule:

```python
#!/usr/bin/env python3
import attune

class TemperatureSensor(attune.PollingSensor):
    def setup(self):
        self.interval = 5.0  # default interval (overridable per-rule)

    def poll(self, rule):
        device = rule.trigger_params.get("device", "/dev/temp0")
        temp = read_temperature(device)
        if temp > 100:
            self.emit({"temperature": temp, "alert": True}, rule=rule)

attune.run_sensor(TemperatureSensor)
```

### Async Polling (`AsyncPollingSensor`)

One asyncio task per active rule (ideal for I/O-bound checks):

```python
#!/usr/bin/env python3
import attune

class ApiSensor(attune.AsyncPollingSensor):
    async def setup(self):
        import httpx
        self.http = httpx.AsyncClient()
        self.interval = 10.0

    async def poll(self, rule):
        url = rule.trigger_params["url"]
        resp = await self.http.get(url)
        if resp.status_code >= 500:
            await self.async_emit({"url": url, "status": resp.status_code}, rule=rule)

    async def cleanup(self):
        await self.http.aclose()

attune.run_sensor(ApiSensor)
```

### Custom Event Loops (`Sensor` base class)

For non-polling sensors, override `run()`:

```python
import attune

class FileTailSensor(attune.Sensor):
    def run(self):
        import time
        path = attune.sensor_context.config.get("watch_path", "/var/log/app.log")
        with open(path) as f:
            f.seek(0, 2)  # seek to end
            while not self.is_shutting_down:
                line = f.readline()
                if line:
                    self.emit({"line": line.strip()})
                else:
                    time.sleep(0.5)

attune.run_sensor(FileTailSensor)
```

### Rule Lifecycle Hooks

All sensor classes support rule lifecycle hooks that fire when the platform
creates, enables, disables, deletes, or updates a rule. Managed sensors
bootstrap from `ATTUNE_SENSOR_TRIGGERS` and then receive live lifecycle deltas
from the notifier WebSocket using `Authorization: Bearer <ATTUNE_API_TOKEN>`
and `trigger_ref:<ref>` subscriptions:

```python
class StatefulSensor(attune.PollingSensor):
    def on_rule_created(self, rule):
        """New rule activated — allocate per-rule resources."""
        self.logger.info("Rule created: %s", rule.rule_ref, extra={"params": rule.trigger_params})

    def on_rule_enabled(self, rule):
        """Previously disabled rule re-enabled."""

    def on_rule_disabled(self, rule):
        """Rule disabled — pause per-rule work."""

    def on_rule_deleted(self, rule):
        """Rule permanently removed — free resources."""

    def on_rule_updated(self, rule, old_params):
        """Rule parameters changed — adapt."""
        self.logger.info("Rule updated: %s → %s", old_params, rule.trigger_params)
```

`PollingSensor` and `AsyncPollingSensor` automatically start/stop per-rule
poll threads/tasks in response to these hooks. Override them to add custom
behavior (call `super()` to keep the auto-management).

Passing `rule=rule` to `emit()` or `async_emit()` targets that numeric rule by
default using `trigger_instance_id="rule_<id>"`. Pass `target_rule=False` only
for an intentional broadcast to every eligible enabled rule for the trigger.

### Managed Sensor Token Rotation

The managed sensor service currently rotates tokens by restarting the sensor
process. It does not inject `ATTUNE_SENSOR_TOKEN_STATE_PATH`. If another runtime
explicitly provides that path, the SDK reads the JSON file on demand. Expected
fields:

```json
{
  "token": "eyJ...",
  "expires_at": "2026-12-31T00:00:00Z"
}
```

Compatibility aliases are also accepted: `api_token` and `token_expires_at`.
If the state file is unavailable, the SDK falls back to the startup
`ATTUNE_API_TOKEN` value when present; otherwise token reads fail clearly.
For Python token-source and failure behavior, see:
[docs/managed-sensor-token-rotation-contract.md](docs/managed-sensor-token-rotation-contract.md).

## Environment Variables

### Actions

| Variable | Description |
|----------|-------------|
| `ATTUNE_ACTION` | Action reference (e.g., `mypack.deploy`) |
| `ATTUNE_PACK_REF` | Pack reference |
| `ATTUNE_EXEC_ID` | Execution database ID |
| `ATTUNE_API_URL` | API base URL |
| `ATTUNE_API_TOKEN` | Execution-scoped API token (optional) |
| `ATTUNE_ARTIFACTS_DIR` | Shared artifact volume path |
| `ATTUNE_RUNTIME_ENVS_DIR` | Runtime environments root |
| `ATTUNE_RULE` | Rule reference (if rule-triggered) |
| `ATTUNE_TRIGGER` | Trigger reference (if event-triggered) |

### Sensors

| Variable | Description |
|----------|-------------|
| `ATTUNE_SENSOR_REF` | Sensor reference |
| `ATTUNE_SENSOR_ID` | Sensor database ID |
| `ATTUNE_API_URL` | API base URL |
| `ATTUNE_API_TOKEN` | Sensor-scoped API token |
| `ATTUNE_PACK_REF` | Pack reference |
| `ATTUNE_ARTIFACTS_DIR` | Shared artifact volume path |
| `ATTUNE_API_TOKEN_EXPIRES_AT` | Optional ISO-8601/epoch expiry metadata for the fallback token |
| `ATTUNE_SENSOR_TOKEN_EXPIRES_AT` | Optional legacy expiry metadata fallback |
| `ATTUNE_SENSOR_TOKEN_STATE_PATH` | Optional externally managed token state file; not injected by the managed service |
| `ATTUNE_SENSOR_TOKEN_RECONNECT_WINDOW_SECONDS` | Optional pre-expiry reconnect window (default `30`) |
| `ATTUNE_NOTIFIER_WS_URL` | Notifier WebSocket URL; remote endpoints require `wss://` by default |
| `ATTUNE_ALLOW_INSECURE_NOTIFIER_WS` | Allow non-loopback `ws://` only on an explicitly trusted development network |
| `ATTUNE_SENSOR_TRIGGERS` | Bootstrap JSON array of managed rule bindings |
| `ATTUNE_SENSOR_TRIGGER_TYPES` | JSON array (or comma-separated fallback) of all trigger refs to subscribe to |
| `ATTUNE_LOG_LEVEL` | Log verbosity |
| `ATTUNE_LOG_FORMAT` | Managed runtime log format |
| `ATTUNE_SENSOR_CONFIG_*` | Caller-supplied values exposed by `sensor_context.config`; persisted sensor config is not injected |

`ATTUNE_SENSOR_TRIGGERS` is a startup snapshot. Ordinary rule changes arrive
in-process through notifier lifecycle envelopes and do not restart the sensor.
If `ATTUNE_SENSOR_TRIGGER_TYPES` is absent, the SDK derives subscriptions from
the bootstrap snapshot.

## Development

```bash
cd python-attune-sdk
pip install -e ".[dev]"
pytest
```

### Regenerating the API Client

The generated client is committed to the repo so users get it out of the box.
To update it after API changes:

```bash
# With a running API:
./scripts/generate-client.sh

# Or from a spec file:
./scripts/generate-client.sh /path/to/openapi.json
```

Requires `openapi-python-client==0.29.0` (included in `[dev]` extras). Generation
is staged in a temporary directory, so a failed generation leaves the committed
client intact.

The contract tests use the checked operation-inventory snapshot by default. To
compare every generated operation directly with a candidate spec, run:

```bash
ATTUNE_OPENAPI_PATH=/path/to/openapi.json pytest tests/test_api_client.py
```

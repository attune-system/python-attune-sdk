# attune — Python SDK for Attune Actions & Sensors

A lightweight Python package providing boilerplate for writing [Attune](https://github.com/AndroxxTraxxon/attune) actions and sensors.

## Installation

```bash
pip install attune-sdk              # includes API client, httpx, attrs
pip install attune-sdk[sensor]      # adds pika for MQ-based sensors
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

**Constructing a client manually** (e.g., outside an execution):

```python
from attune.api_client import AuthenticatedClient
client = AuthenticatedClient(base_url="http://localhost:8080", token="your-token")
```

All API modules live under `attune.api_client.api.<domain>` and all request/response
models under `attune.api_client.models`.

## Writing Sensors

Sensors are long-running processes that emit events. The SDK provides rule
lifecycle management, signal handling (SIGINT/SIGTERM), and MQ integration
out of the box.

The sensor context is a module-level singleton, accessible anywhere:

```python
import attune

# attune.sensor_context is available at import time
print(attune.sensor_context.sensor_ref)
print(attune.sensor_context.api_url)
print(attune.sensor_context.config)  # ATTUNE_SENSOR_CONFIG_* vars
```

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
            self.emit({"url": url, "status": resp.status_code}, rule=rule)

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
creates, enables, disables, deletes, or updates a rule:

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
| `ATTUNE_RULE` | Rule reference (if rule-triggered) |
| `ATTUNE_TRIGGER` | Trigger reference (if event-triggered) |

### Sensors

| Variable | Description |
|----------|-------------|
| `ATTUNE_SENSOR_REF` | Sensor reference |
| `ATTUNE_SENSOR_ID` | Sensor database ID |
| `ATTUNE_API_URL` | API base URL |
| `ATTUNE_API_TOKEN` | Sensor-scoped API token |
| `ATTUNE_MQ_URL` | RabbitMQ connection URL |
| `ATTUNE_MQ_EXCHANGE` | RabbitMQ exchange name |
| `ATTUNE_LOG_LEVEL` | Log verbosity |

## Development

```bash
cd packs.external/python-attune
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

Requires `openapi-python-client` (included in `[dev]` extras).

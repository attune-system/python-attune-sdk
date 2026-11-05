# Sensor startup migration for Attune 0.10.2

SDK 0.5.6 uses environment variables for sensor configuration and initial rule
bindings. Attune 0.10.2 delivers those values through a single stdin JSON object
and closes the pipe. An environment-based SDK can therefore start without its
configuration or rules. Updating the server or regenerating the SDK's OpenAPI
client does not update the sensor lifecycle implementation in an installed SDK.

SDK 0.5.7 is the first release with the stdin startup contract. Pin Python
sensor dependencies to `attune-sdk[sensor]==0.5.7` when migrating from 0.5.6.

Use an SDK build containing `attune.sensor_bootstrap`, the lazy
`SensorContext.bootstrap_state`, and the stdin-based `Sensor._bootstrap_rules`.
This release implements that contract. Do not assume an existing
PyPI release contains it based on the generated API client version.

The package publish workflow verifies the built wheel's startup behavior before
uploading it. The release used for migration must include both the bootstrap
implementation and that verification. SDK 0.5.6 is not a migration target;
do not leave permissive requirements such as `attune-sdk[sensor]>=0.1.0`
unchanged and expect them to enforce this contract.

## Update the actual sensor environment

1. Build and distribute a wheel from the reviewed SDK source, or use a published
   SDK release confirmed to include this change. For a source build, run
   `python -m pip wheel --no-deps --wheel-dir /tmp/attune-sdk-wheels .` from
   the SDK repository.
2. Update each Python sensor pack's SDK dependency to that release or to an
   immutable source commit containing the change. For example, a source
   requirement has the form
   `attune-sdk[sensor] @ git+https://github.com/attune-system/python-attune-sdk.git@<commit-sha>`.
   Replace `<commit-sha>` with the reviewed commit; a branch name is not a pin.
3. Rebuild the pack runtime environment. Updating a requirements file or the
   host Python installation alone does not replace an SDK already installed in
   an existing sensor environment. If installing a local wheel for testing,
   use that environment's Python and `pip install --force-reinstall` so a source
   build with unchanged package metadata replaces the old installation.
4. Restart the sensor so it receives a fresh bootstrap and verify that its
   initial active rules are present. Run the SDK's
   `tests/test_sensor_startup_contract.py` against the candidate installation
   before rollout; it exercises both synchronous and asynchronous startup.

Do not edit generated index dependency metadata to force a newer SDK. Update
the source pack requirements and publish a new immutable pack version, then
refresh the index so its source checksums and dependency metadata agree.

Check the SDK in the sensor runtime environment, using that environment's
interpreter rather than the host Python:

```sh
python -c 'import attune; from attune.sensor_bootstrap import SensorBootstrapState; print(attune.__version__, attune.__file__)'
```

An import failure means that environment still lacks the stdin-capable SDK.
Successful import identifies the candidate installation; the startup tests
above verify its behavior.

No sensor subclass changes are required when using `attune.run_sensor` and
`self.config` or `attune.sensor_context.config`. Values now retain their JSON
types: for example, `false` is a Python `False`, not an environment string.
Code that reads `ATTUNE_SENSOR_CONFIG_*` or `ATTUNE_SENSOR_TRIGGERS` directly
must instead use the SDK context and rule hooks.

## Custom launchers

Pass stdin through to the sensor process. Write exactly one object with these
two sections and close stdin after the complete object:

```json
{
  "config": {"enabled": false, "interval": 10},
  "triggers": [
    {"id": 42, "ref": "example.rule", "trigger_ref": "example.trigger", "config": {"interval": 3}}
  ]
}
```

The delivery limit is 32 MiB. Empty values use `{"config": {}, "triggers": []}`;
empty stdin is an error. The SDK caches the frame so config and initial rule
bindings share one read. Importing the SDK does not consume action stdin.
Credentials and process identity still arrive through their documented
environment variables. Do not copy sensor values back into environment
variables: both configuration and rule parameters can contain secrets.

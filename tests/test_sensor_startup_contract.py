"""Exercise the managed startup contract through real process stdin and EOF."""

import json
import os
import subprocess
import sys
import textwrap

import pytest


@pytest.mark.parametrize("asynchronous", [False, True])
def test_public_entrypoint_uses_one_bootstrap_for_config_and_rules(asynchronous):
    setup = "async def setup(self):" if asynchronous else "def setup(self):"
    base = "AsyncPollingSensor" if asynchronous else "Sensor"
    program = f"""
import json
import attune

class Probe(attune.{base}):
    def _start_lifecycle_listener(self):
        return None

    def on_rule_created(self, rule):
        # Rule hooks can access config before setup; both use the same frame.
        assert self.config["enabled"] is False

    {setup}
        rule = self.rules[42]
        print(json.dumps({{"config": self.config, "params": rule.trigger_params}}))
        self.shutdown()

attune.run_sensor(Probe)
"""
    bootstrap = {
        "config": {"enabled": False, "count": 0, "nested": ["private-fixture"]},
        "triggers": [{
            "id": 42,
            "ref": "probe.rule",
            "trigger_ref": "probe.trigger",
            "config": {"interval": 3, "enabled": False},
        }],
    }
    result = subprocess.run(
        [sys.executable, "-c", program],
        input=json.dumps(bootstrap),
        capture_output=True,
        text=True,
        timeout=15,
        env={
            **os.environ,
            "ATTUNE_SENSOR_CONFIG_ENABLED": "stale-env-value",
            "ATTUNE_SENSOR_TRIGGERS": "[]",
        },
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "config": bootstrap["config"],
        "params": bootstrap["triggers"][0]["config"],
    }
    assert "private-fixture" not in result.stderr


def test_sdk_import_does_not_consume_action_stdin():
    result = subprocess.run(
        [sys.executable, "-c", textwrap.dedent("""
            import attune
            def action(message):
                return {"message": message}
            attune.run_action(action)
        """)],
        input='{"message": "action-input"}',
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"message": "action-input"}


def test_missing_bootstrap_fails_startup_with_migration_diagnostic():
    result = subprocess.run(
        [sys.executable, "-c", "import attune; attune.run_sensor(attune.Sensor)"],
        input="",
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 1
    assert "Missing sensor stdin bootstrap" in result.stderr
    assert "Sensor started" not in result.stderr

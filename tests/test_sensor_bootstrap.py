from io import BytesIO

import pytest

from attune.sensor_bootstrap import MAX_BOOTSTRAP_BYTES, SensorBootstrapState, read_sensor_bootstrap


def test_bootstrap_is_lazy_cached_and_preserves_value_types():
    reader = BytesIO(b'{"config": {"count": 0, "enabled": false, "nested": ["private", {"text": ""}]}, "triggers": []}')
    state = SensorBootstrapState(reader)
    assert reader.tell() == 0
    bootstrap = state.get()
    assert bootstrap.config["count"] == 0
    assert bootstrap.config["enabled"] is False
    assert state.get() is bootstrap
    assert "private" not in repr(bootstrap)


@pytest.mark.parametrize("raw", [b'', b'private-credential-fixture', b'{"config": [], "triggers": []}', b'{"config": {}, "triggers": [], "extra": true}'])
def test_invalid_bootstraps_fail_without_echoing_values(raw):
    with pytest.raises(ValueError) as failure:
        read_sensor_bootstrap(BytesIO(raw))
    assert "private-credential-fixture" not in str(failure.value)


def test_oversized_bootstrap_is_rejected_before_parsing():
    with pytest.raises(ValueError, match="delivery limit"):
        read_sensor_bootstrap(BytesIO(b' ' * (MAX_BOOTSTRAP_BYTES + 1)))

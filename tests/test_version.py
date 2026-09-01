from importlib.metadata import version

import attune


def test_runtime_version() -> None:
    assert attune.__version__ == "0.4.0"


def test_distribution_metadata_matches_runtime_version() -> None:
    assert version("attune-sdk") == attune.__version__

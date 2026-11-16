from pathlib import Path

import pytest


@pytest.fixture
def sample_contract():
    return (Path(__file__).resolve().parents[1] / "test-data" / "sample_contract.txt").read_text(encoding="utf-8")

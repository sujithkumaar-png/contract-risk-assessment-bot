"""Future browser tests use pytest-playwright's isolated page/context fixtures."""
import os

import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "base_url": os.getenv("UI_BASE_URL", "http://127.0.0.1:8501"),
            "viewport": {"width": 1280, "height": 800}}

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


@pytest.fixture
def platform_client():
    with TestClient(create_app(Settings(environment="test"))) as client:
        yield client

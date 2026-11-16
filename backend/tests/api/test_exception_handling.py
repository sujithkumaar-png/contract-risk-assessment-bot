"""Regression coverage for framework errors and private application failures."""
from io import StringIO
import json
import logging

from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import JsonFormatter
from contract_risk.api import app as legacy_app

pytestmark = pytest.mark.api


@pytest.fixture
def application_logs(monkeypatch):
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    monkeypatch.setattr(logging.getLogger("contract_risk.platform"), "handlers", [handler])
    try:
        yield stream
    finally:
        handler.close()


@pytest.mark.parametrize("exception_type", [HTTPException, StarletteHTTPException])
@pytest.mark.parametrize("status", [400, 409, 429])
def test_expected_http_errors_keep_status_detail_and_headers(
    platform_client, application_logs, exception_type, status
):
    @platform_client.app.get("/test-http-error")
    def expected_error():
        raise exception_type(status_code=status, detail={"reason": "expected"},
                             headers={"Retry-After": "30"})

    response = platform_client.get("/test-http-error", headers={"X-Request-ID": "expected-check"})
    assert response.status_code == status
    assert response.json() == {"detail": {"reason": "expected"}}
    assert response.headers["Retry-After"] == "30"
    assert response.headers["X-Request-ID"] == "expected-check"
    records = [json.loads(line) for line in application_logs.getvalue().splitlines()]
    assert [record["event"] for record in records] == ["http_request"]
    assert records[0]["status"] == status


@pytest.mark.parametrize("payload", [{}, {"contract_text": ""}, {"contract_text": None}])
def test_validation_contract_matches_legacy_api(platform_client, application_logs, payload):
    with TestClient(legacy_app) as legacy_client:
        expected = legacy_client.post("/api/v1/analyze", json=payload)
    response = platform_client.post("/api/v1/analyze", json=payload,
                                    headers={"X-Request-ID": "validation-check"})
    assert response.status_code == expected.status_code == 422
    assert response.json() == expected.json()
    assert response.headers["X-Request-ID"] == "validation-check"
    records = [json.loads(line) for line in application_logs.getvalue().splitlines()]
    assert [record["event"] for record in records] == ["http_request"]


def test_unexpected_exception_logs_class_and_id_without_sensitive_values(platform_client, application_logs):
    @platform_client.app.post("/test-failure/{document_id}")
    def unexpected_error(document_id: str):
        raise RuntimeError("credential-message-secret")

    response = platform_client.post(
        "/test-failure/private-document?token=private-token",
        headers={"X-Request-ID": "diagnostic-check", "Authorization": "Bearer private-credential"},
        json={"contract_text": "private-contract-content"},
    )
    assert response.status_code == 500
    assert response.headers["X-Request-ID"] == "diagnostic-check"
    assert response.json() == {"detail": "Internal server error", "request_id": "diagnostic-check"}
    raw_logs = application_logs.getvalue()
    records = [json.loads(line) for line in raw_logs.splitlines()]
    assert [record["event"] for record in records] == ["unexpected_application_error", "http_request"]
    error, request = records
    assert set(error) == {"timestamp", "level", "event", "exception_class", "request_id"}
    assert error["level"] == "ERROR"
    assert error["exception_class"] == "RuntimeError"
    assert error["request_id"] == request["request_id"] == "diagnostic-check"
    assert request["method"] == "POST"
    assert request["route"] == "/test-failure/{document_id}"
    assert request["status"] == 500
    assert isinstance(request["duration_ms"], (int, float)) and request["duration_ms"] >= 0
    for sensitive in ["credential-message-secret", "private-document", "private-token",
                      "private-credential", "private-contract-content", "Traceback"]:
        assert sensitive not in raw_logs
        assert sensitive not in response.text

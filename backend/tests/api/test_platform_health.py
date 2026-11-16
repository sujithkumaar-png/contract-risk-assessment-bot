import pytest

pytestmark = pytest.mark.api


def test_liveness(platform_client):
    response = platform_client.get("/api/v1/health/live", headers={"X-Request-ID": "health-check-1"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "health-check-1"
    assert response.json() == {"status": "ok", "check": "liveness", "request_id": "health-check-1", "dependencies": {}}


def test_readiness_does_not_claim_database(platform_client):
    response = platform_client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json()["dependencies"] == {"startup": "ok", "risk_engine": "ok", "database": "not_configured"}
    assert response.json()["request_id"] == response.headers["X-Request-ID"]


def test_engine_failure_makes_readiness_fail_but_not_liveness(platform_client, monkeypatch):
    monkeypatch.setattr("app.api.health.check_risk_engine", lambda: False)
    response = platform_client.get("/api/v1/health/ready")
    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["dependencies"]["risk_engine"] == "failed"
    assert platform_client.get("/api/v1/health/live").status_code == 200


def test_startup_required_for_readiness(platform_client):
    platform_client.app.state.started = False
    assert platform_client.get("/api/v1/health/ready").status_code == 503


@pytest.mark.parametrize("request_id", ["bad id", "x" * 65, ""])
def test_invalid_request_id_is_replaced(platform_client, request_id):
    from uuid import UUID
    response = platform_client.get("/api/v1/health/live", headers={"X-Request-ID": request_id})
    assert str(UUID(response.headers["X-Request-ID"])) == response.json()["request_id"]


def test_validation_and_not_found_have_request_ids(platform_client):
    for response in [platform_client.post("/api/v1/analyze", json={}), platform_client.get("/missing")]:
        assert response.status_code in (422, 404)
        assert response.headers["X-Request-ID"]


def test_unexpected_error_is_sanitized_and_has_request_id(platform_client):
    @platform_client.app.get("/test-error")
    def broken():
        raise RuntimeError("private-configuration-value")

    response = platform_client.get("/test-error", headers={"X-Request-ID": "failure-check"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error", "request_id": "failure-check"}
    assert response.headers["X-Request-ID"] == "failure-check"


def test_request_logging_excludes_body_and_query(platform_client, monkeypatch):
    import logging
    events = []
    monkeypatch.setattr(logging.getLogger("contract_risk.platform"), "info",
                        lambda event, **kwargs: events.append((event, kwargs)))
    response = platform_client.post("/api/v1/analyze?token=secret-query-value",
                                    json={"contract_text": "private-contract-value"})
    assert response.status_code == 200
    event, details = events[-1]
    assert event == "http_request"
    assert details["extra"]["route"] == "/api/v1/analyze"
    assert details["extra"]["request_id"] == response.headers["X-Request-ID"]
    assert "secret-query-value" not in str(events)
    assert "private-contract-value" not in str(events)

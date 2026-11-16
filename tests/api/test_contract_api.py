from fastapi.testclient import TestClient
import pytest
from contract_risk.api import app

pytestmark = pytest.mark.api


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_endpoint_returns_expected_sample_result(client):
    response = client.post("/api/v1/analyze", json={
        "contract_text": "termination without notice; unlimited liability; confidentiality; arbitration"
    })
    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 8
    assert body["overall_risk"] == "High Risk"
    assert body["detected_count"] == 4
    assert len(body["findings"]) == 4


def test_analyze_endpoint_rejects_empty_text(client):
    response = client.post("/api/v1/analyze", json={"contract_text": ""})
    assert response.status_code == 422


def test_analyze_endpoint_rejects_missing_field(client):
    response = client.post("/api/v1/analyze", json={})
    assert response.status_code == 422


@pytest.mark.parametrize("value", [None, 42, True, [], {}])
def test_analyze_rejects_non_string_values(client, value):
    response = client.post("/api/v1/analyze", json={"contract_text": value})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "contract_text"]
    assert error["type"] == "string_type"


def test_analyze_rejects_malformed_json(client):
    response = client.post("/api/v1/analyze", content="{", headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "json_invalid"


@pytest.mark.parametrize(("text", "score", "risk", "findings"), [
    ("Ordinary delivery terms.", 0, "Low Risk", []),
    ("INDEMNITY indemnity; confidentiality", 3, "Low Risk", [
        {"clause": "indemnity", "level": "Medium", "points": 2},
        {"clause": "confidentiality", "level": "Low", "points": 1},
    ]),
])
def test_analyze_response_contract(client, text, score, risk, findings):
    response = client.post("/api/v1/analyze", json={"contract_text": text})
    assert response.status_code == 200
    assert response.json() == {"findings": findings, "score": score,
                               "overall_risk": risk, "detected_count": len(findings)}


def test_whitespace_is_currently_valid_api_text(client):
    # Preserve the existing min_length contract; the UI rejects whitespace separately.
    response = client.post("/api/v1/analyze", json={"contract_text": "   "})
    assert response.status_code == 200
    assert response.json()["score"] == 0

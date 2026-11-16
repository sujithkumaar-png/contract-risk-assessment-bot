def test_platform_reuses_original_sample_behavior(platform_client):
    response = platform_client.post("/api/v1/analyze", json={"contract_text": "termination without notice; unlimited liability; confidentiality; arbitration"})
    assert response.status_code == 200
    body = response.json()
    assert (body["detected_count"], body["score"], body["overall_risk"]) == (4, 8, "High Risk")
    assert platform_client.get("/health").json() == {"status": "ok"}

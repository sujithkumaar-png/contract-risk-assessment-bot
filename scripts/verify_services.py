"""Start real local servers, verify HTTP responses, then stop owned processes."""
import json
from pathlib import Path
import socket
import subprocess
import sys
import time

import httpx

ROOT = Path(__file__).resolve().parents[1]


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def verify(name, arguments, checks):
    port = free_port()
    log_path = ROOT / "reports" / f"{name}-startup.log"
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen([sys.executable, "-m", *arguments, str(port)], cwd=ROOT,
                                   stdout=log, stderr=subprocess.STDOUT)
        try:
            with httpx.Client(base_url=f"http://127.0.0.1:{port}", trust_env=False) as client:
                for _ in range(100):
                    if process.poll() is not None:
                        raise RuntimeError(f"{name} exited; see {log_path}")
                    try:
                        response = client.get(checks[0])
                        if response.status_code == 200:
                            break
                    except httpx.TransportError:
                        pass
                    time.sleep(0.2)
                else:
                    raise TimeoutError(f"{name} did not become ready")
                checks[1](client)
        finally:
            process.terminate()
            process.wait(timeout=15)


def check_api(client):
    response = client.get("/health")
    assert response.status_code == 200 and response.json() == {"status": "ok"}
    sample = (ROOT / "test-data" / "sample_contract.txt").read_text(encoding="utf-8")
    for payload, status in [({"contract_text": sample}, 200), ({"contract_text": ""}, 422),
                            ({}, 422), ({"contract_text": 12}, 422),
                            ({"contract_text": "Ordinary terms"}, 200)]:
        result = client.post("/api/v1/analyze", json=payload)
        assert result.status_code == status
        if payload.get("contract_text") == sample:
            body = result.json()
            assert (body["score"], body["detected_count"], body["overall_risk"]) == (8, 4, "High Risk")
        if payload.get("contract_text") == "Ordinary terms":
            assert result.json() == {"score": 0, "findings": [], "detected_count": 0, "overall_risk": "Low Risk"}
        print("API", status, json.dumps(result.json()))
    response = client.get("/docs")
    assert response.status_code == 200
    print("API health and Swagger: 200")


def check_streamlit(client):
    assert client.get("/_stcore/health").text == "ok"
    response = client.get("/")
    assert response.status_code == 200 and "<html" in response.text.lower()
    print("Streamlit health and homepage shell: 200 (widget behavior tested separately via AppTest)")


if __name__ == "__main__":
    (ROOT / "reports").mkdir(exist_ok=True)
    verify("api", ["uvicorn", "contract_risk.api:app", "--app-dir", "src", "--host", "127.0.0.1", "--port"], ("/health", check_api))
    verify("streamlit", ["streamlit", "run", "src/contract_risk/streamlit_app.py", "--server.headless", "true", "--server.address", "127.0.0.1", "--server.port"], ("/_stcore/health", check_streamlit))

"""Sequential HTTP smoke checks for the foundation; requires a frontend build."""
from contextlib import contextmanager
import json
from pathlib import Path
import socket
import subprocess
import sys
import time

import httpx

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def server(name, command, cwd):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    (ROOT / "reports").mkdir(exist_ok=True)
    with (ROOT / "reports" / f"platform-{name}.log").open("w", encoding="utf-8") as log:
        process = subprocess.Popen([*command, str(port)], cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
        try:
            with httpx.Client(base_url=f"http://127.0.0.1:{port}", trust_env=False, timeout=3) as client:
                for _ in range(100):
                    if process.poll() is not None:
                        raise RuntimeError(f"{name} exited; see reports/platform-{name}.log")
                    try:
                        if client.get("/").status_code < 500:
                            break
                    except httpx.TransportError:
                        pass
                    time.sleep(0.2)
                else:
                    raise TimeoutError(f"{name} not available")
                yield client
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def main():
    with server("backend", [sys.executable, "-m", "uvicorn", "app.main:app", "--app-dir", "backend/src",
                            "--host", "127.0.0.1", "--no-access-log", "--port"], ROOT) as client:
        for check in ("live", "ready"):
            response = client.get(f"/api/v1/health/{check}", headers={"X-Request-ID": "smoke-check"})
            assert response.status_code == 200
            assert response.json()["request_id"] == response.headers["X-Request-ID"] == "smoke-check"
            print(check, json.dumps(response.json()))
        assert client.get("/api/v1/health/ready").json()["dependencies"]["database"] == "not_configured"
        response = client.post("/api/v1/analyze", json={"contract_text": (ROOT / "test-data/sample_contract.txt").read_text(encoding="utf-8")})
        assert response.status_code == 200
        body = response.json()
        assert (body["score"], body["detected_count"], body["overall_risk"]) == (8, 4, "High Risk")
        assert client.get("/health").json() == {"status": "ok"}
        print("Legacy API preserved: sample score 8, four findings, High Risk")
    # Run Node directly to keep process cleanup limited to the actual owned server.
    with server("frontend", ["node", "node_modules/next/dist/bin/next", "start", "--hostname", "127.0.0.1", "--port"], ROOT / "frontend") as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "contract risk." in response.text.lower()
        assert "Illustrative sample" in response.text
        assert "_next/static/" in response.text
        print("Frontend production homepage: HTTP 200; landing content and asset references present")


if __name__ == "__main__":
    main()

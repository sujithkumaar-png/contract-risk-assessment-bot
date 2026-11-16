from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok", "not_ready"]
    check: Literal["liveness", "readiness"]
    request_id: str
    dependencies: dict[str, Literal["ok", "failed", "not_configured"]]

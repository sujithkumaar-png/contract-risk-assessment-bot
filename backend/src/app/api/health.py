from fastapi import APIRouter, Request, Response

from app.schemas.health import HealthResponse
from app.services.readiness import check_risk_engine

router = APIRouter(prefix="/api/v1/health", tags=["Platform health"])


@router.get("/live", response_model=HealthResponse)
def live(request: Request) -> HealthResponse:
    return HealthResponse(status="ok", check="liveness", request_id=request.state.request_id,
                          dependencies={})


@router.get("/ready", response_model=HealthResponse, responses={503: {"model": HealthResponse}})
def ready(request: Request, response: Response) -> HealthResponse:
    engine_ok = check_risk_engine()
    startup_ok = request.app.state.started
    is_ready = engine_ok and startup_ok
    response.status_code = 200 if is_ready else 503
    return HealthResponse(
        status="ok" if is_ready else "not_ready", check="readiness",
        request_id=request.state.request_id,
        dependencies={"startup": "ok" if startup_ok else "failed",
                      "risk_engine": "ok" if engine_ok else "failed",
                      "database": "not_configured"},
    )

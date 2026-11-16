"""Platform entry point; compose rather than copy the existing analysis API."""
from contextlib import asynccontextmanager
import re
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from contract_risk.api import app as legacy_app
from app.api.health import router as health_router
from app.core.config import Settings
from app.core.logging import configure_logging


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings if settings is not None else Settings.from_env()
    logger = configure_logging(config.log_level)

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        application.state.started = True
        logger.info("application_started")
        try:
            yield
        finally:
            application.state.started = False
            logger.info("application_stopped")

    application = FastAPI(title="Contract Risk Assessment Platform", version="0.1.0", lifespan=lifespan)
    application.state.settings = config
    application.state.started = False

    @application.middleware("http")
    async def request_context(request: Request, call_next):
        supplied = request.headers.get("X-Request-ID", "")
        request_id = supplied if re.fullmatch(r"[A-Za-z0-9_-]{1,64}", supplied) else str(uuid4())
        request.state.request_id = request_id
        start = perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:
            # FastAPI handles expected HTTP/validation errors inside call_next.
            # Only log the type of an unexpected error, never its text/traceback.
            logger.error("unexpected_application_error", extra={
                "exception_class": type(exc).__name__, "request_id": request_id,
            })
            # Do not expose exception messages, payloads or configuration values.
            response = JSONResponse(status_code=500, content={"detail": "Internal server error", "request_id": request_id})
        response.headers["X-Request-ID"] = request_id
        route = request.scope.get("route")
        logger.info("http_request", extra={"request_id": request_id, "method": request.method,
                    "route": getattr(route, "path", "unmatched"), "status": response.status_code,
                    "duration_ms": round((perf_counter() - start) * 1000, 2)})
        return response

    application.include_router(health_router)
    application.include_router(legacy_app.router)
    return application


app = create_app()

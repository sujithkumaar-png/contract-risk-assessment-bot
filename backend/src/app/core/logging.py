"""JSON application logs without request bodies, query strings or credentials."""
from datetime import datetime, timezone
import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {"timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname, "event": record.getMessage()}
        for key in ("request_id", "method", "route", "status", "duration_ms", "exception_class"):
            if hasattr(record, key):
                data[key] = getattr(record, key)
        return json.dumps(data)


def configure_logging(level: str) -> logging.Logger:
    logger = logging.getLogger("contract_risk.platform")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger

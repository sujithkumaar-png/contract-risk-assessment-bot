import json
import logging
from io import StringIO

from app.core.logging import JsonFormatter
from app.core.config import Settings
from app.main import create_app


def test_json_formatter_emits_request_metadata():
    record = logging.LogRecord("test", logging.INFO, "", 0, "http_request", (), None)
    record.request_id = "test-request"
    record.status = 200
    payload = json.loads(JsonFormatter().format(record))
    assert payload["event"] == "http_request"
    assert payload["level"] == "INFO"
    assert payload["request_id"] == "test-request"
    assert payload["status"] == 200
    assert payload["timestamp"].endswith("+00:00")


def test_repeated_app_creation_reuses_one_json_handler(monkeypatch):
    logger = logging.getLogger("contract_risk.platform")
    monkeypatch.setattr(logger, "handlers", [])
    stream = StringIO()
    try:
        for _ in range(5):
            create_app(Settings(environment="test"))
        assert len(logger.handlers) == 1
        handler = logger.handlers[0]
        assert isinstance(handler.formatter, JsonFormatter)
        assert logger.propagate is False
        handler.setStream(stream)
        logger.info("handler_reuse_check", extra={"request_id": "one-record"})
        records = [json.loads(line) for line in stream.getvalue().splitlines()]
        assert len(records) == 1
        assert records[0]["event"] == "handler_reuse_check"
        assert records[0]["request_id"] == "one-record"
    finally:
        for handler in logger.handlers:
            handler.close()

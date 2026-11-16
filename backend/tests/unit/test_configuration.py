import pytest

from app.core.config import ConfigurationError, Settings
from app.services.readiness import check_risk_engine

pytestmark = pytest.mark.unit


def test_safe_defaults_require_no_secrets():
    settings = Settings.from_env({})
    assert settings.environment == "development"
    assert settings.log_level == "INFO"


def test_supported_configuration():
    settings = Settings.from_env({"APP_ENV": "production", "LOG_LEVEL": "WARNING"})
    assert settings.environment == "production"
    assert settings.log_level == "WARNING"


@pytest.mark.parametrize("key", ["APP_ENV", "LOG_LEVEL"])
def test_invalid_configuration_does_not_echo_value(key):
    secret = "sensitive-input-do-not-log"
    with pytest.raises(ConfigurationError) as error:
        Settings.from_env({key: secret})
    assert secret not in str(error.value)
    assert "Invalid configuration fields:" in str(error.value)


def test_engine_exception_is_not_ready(monkeypatch):
    def broken(_):
        raise RuntimeError("sensitive exception")
    monkeypatch.setattr("app.services.readiness.analyze_contract", broken)
    assert check_risk_engine() is False

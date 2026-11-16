"""Small environment boundary; validation errors never echo supplied values."""
import os
from typing import Literal, Mapping

from pydantic import BaseModel, ValidationError


class ConfigurationError(ValueError):
    """Safe startup failure for invalid configuration."""


class Settings(BaseModel):
    environment: Literal["development", "test", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "Settings":
        source = os.environ if environ is None else environ
        values = {field: source[key] for field, key in
                  [("environment", "APP_ENV"), ("log_level", "LOG_LEVEL")] if key in source}
        try:
            return cls.model_validate(values)
        except ValidationError as exc:
            fields = ", ".join(sorted({str(error["loc"][0]) for error in exc.errors()}))
            raise ConfigurationError(f"Invalid configuration fields: {fields}") from None

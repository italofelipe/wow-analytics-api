"""Config validada no boot da API via pydantic-settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Na Vercel usamos o pooler (transaction mode, porta 6543).
    # `statement_cache_size=0` é ligado no deps.py — PgBouncer transaction
    # mode não aceita prepared statements.
    database_url_pooled: SecretStr
    api_allowed_origins: str = "http://localhost:3000"
    sentry_dsn_api: SecretStr | None = None
    sentry_environment: str = "development"
    pool_min_size: int = Field(default=1, ge=1)
    pool_max_size: int = Field(default=5, ge=1, le=20)

    @property
    def allowed_origins(self) -> list[str]:
        return [o.strip() for o in self.api_allowed_origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> ApiSettings:
    return ApiSettings()  # type: ignore[call-arg]

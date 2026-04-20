"""Configuração validada no boot via pydantic-settings.

Carrega de env vars (e de `.env` em dev). Se uma var obrigatória estiver
ausente o processo falha imediatamente, evitando pipelines que quebram
no meio de um run de 20 min.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class IngestionSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Blizzard
    blizzard_client_id: SecretStr
    blizzard_client_secret: SecretStr
    blizzard_regions: str = "us,eu"

    # Raider.IO
    raiderio_base_url: HttpUrl = Field(default=HttpUrl("https://raider.io/api/v1"))
    raiderio_user_agent: str = "wow-analytics/0.1"

    # Postgres (ingestor usa connection direta — não pooler)
    database_url: SecretStr

    # R2
    r2_account_id: SecretStr
    r2_access_key_id: SecretStr
    r2_secret_access_key: SecretStr
    r2_bucket: str = "wow-analytics-raw"
    r2_endpoint: HttpUrl

    # Observability
    sentry_dsn_api: SecretStr | None = None
    sentry_environment: str = "development"

    # Tunables
    ingest_concurrency: int = Field(default=8, ge=1, le=20)
    ingest_snapshot_limit: int = Field(default=500, ge=1)
    ingest_run_id: str | None = None
    log_level: str = "INFO"
    log_format: Literal["json", "console"] = "json"

    @property
    def regions_list(self) -> list[str]:
        return [r.strip().lower() for r in self.blizzard_regions.split(",") if r.strip()]


@lru_cache(maxsize=1)
def get_settings() -> IngestionSettings:
    """Singleton cached. Ler via DI nos pipelines, não como global em módulos de domínio."""
    return IngestionSettings()  # type: ignore[call-arg]

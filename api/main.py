"""FastAPI entrypoint.

- Lifespan abre/fecha o pool do asyncpg (conectado via Supabase pooler).
- CORS restrito aos domínios em API_ALLOWED_ORIGINS.
- Sentry inicializa só se `SENTRY_DSN_API` estiver presente.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import get_settings
from api.routers import health

if TYPE_CHECKING:
    pass


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    _maybe_init_sentry(settings)

    # Import local pra manter o módulo importável sem asyncpg (ex. mypy rodando
    # sem o grupo [api]). No runtime o pacote está garantido.
    import asyncpg  # noqa: PLC0415

    pool = await asyncpg.create_pool(
        dsn=settings.database_url_pooled.get_secret_value(),
        min_size=settings.pool_min_size,
        max_size=settings.pool_max_size,
        # Supabase pooler (transaction mode) não suporta prepared statements.
        statement_cache_size=0,
    )
    app.state.db_pool = pool
    try:
        yield
    finally:
        await pool.close()


def _maybe_init_sentry(settings: object) -> None:
    dsn = getattr(settings, "sentry_dsn_api", None)
    if dsn is None:
        return
    try:
        import sentry_sdk  # noqa: PLC0415
    except ImportError:
        return
    sentry_sdk.init(
        dsn=dsn.get_secret_value(),
        environment=getattr(settings, "sentry_environment", "development"),
        traces_sample_rate=0.1,
    )


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="WoW Analytics API",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    return app


app = create_app()

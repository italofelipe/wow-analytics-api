"""Dependências compartilhadas: pool do Postgres gerenciado pelo lifespan.

Uso em routers:

    from api.deps import DbPool

    @router.get("/foo")
    async def foo(pool: DbPool) -> ...:
        async with pool.acquire() as conn:
            ...

O pool não é um singleton importável; vem via dependency override pronta pra teste.
"""

from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, Request

if TYPE_CHECKING:  # evita import pesado se o runtime não tiver asyncpg (dev)
    import asyncpg


def _get_pool(request: Request) -> "asyncpg.Pool":
    pool = getattr(request.app.state, "db_pool", None)
    if pool is None:
        raise RuntimeError("DB pool not initialized (lifespan missing?)")
    return pool  # type: ignore[no-any-return]


DbPool = Annotated["asyncpg.Pool", Depends(_get_pool)]

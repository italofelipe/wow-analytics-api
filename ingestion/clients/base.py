"""Protocol comum para clients de APIs externas + rate limiter compartilhado."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any, Protocol, runtime_checkable
from collections.abc import AsyncIterator


@runtime_checkable
class WoWDataSource(Protocol):
    """Contrato mínimo esperado de qualquer fonte de dados de WoW.

    Implementações (Blizzard, Raider.IO, WarcraftLogs) expõem os métodos que
    fazem sentido para cada uma — este Protocol serve como documentação viva
    e gate para substituições em testes (`respx` + fake).
    """

    async def aclose(self) -> Any: ...


class RateLimiter:
    """Semaphore assíncrono para limitar concorrência global.

    Usar um limiter por client (não global no processo) — cada API tem seu
    próprio budget. Valor padrão é conservador: Blizzard permite 10 req/s;
    ficamos em 8 pra ter margem em 429 + bursts de retry.
    """

    def __init__(self, concurrency: int) -> None:
        self._sem = asyncio.Semaphore(concurrency)

    @asynccontextmanager
    async def slot(self) -> AsyncIterator[None]:
        async with self._sem:
            yield

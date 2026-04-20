"""Repositório concreto de personagens — adapter de saída para Postgres.

Implementa CharactersPort. Stub da Fase 1; substituir o corpo de cada
método quando as migrations estiverem prontas.
"""

from __future__ import annotations

import asyncpg  # noqa: F401 — importado em Fase 1

from ingestion.domain import Character, CharacterRef
from ingestion.ports.characters import CharactersPort  # noqa: F401 — para type hints


class PgCharactersRepo:
    """Implementação Postgres de CharactersPort.

    Recebe um asyncpg.Connection (ou pool) via construtor — sem singletons.
    """

    def __init__(self, conn: "asyncpg.Connection") -> None:  # type: ignore[name-defined]
        self._conn = conn

    async def upsert(self, character: Character) -> None:
        raise NotImplementedError("Fase 1")

    async def find(self, ref: CharacterRef) -> Character | None:
        raise NotImplementedError("Fase 1")

    async def list_for_snapshot(self, limit: int = 500) -> list[CharacterRef]:
        raise NotImplementedError("Fase 1")

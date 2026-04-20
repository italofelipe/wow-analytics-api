"""Repositório concreto da discovery queue — adapter de saída para Postgres."""

from __future__ import annotations

from collections.abc import Iterable

import asyncpg  # noqa: F401

from ingestion.domain import CharacterRef


class PgDiscoveryQueueRepo:
    def __init__(self, conn: "asyncpg.Connection") -> None:  # type: ignore[name-defined]
        self._conn = conn

    async def enqueue_many(self, refs: Iterable[CharacterRef], priority: int = 0) -> int:
        raise NotImplementedError("Fase 1")

    async def next_batch(self, limit: int) -> list[CharacterRef]:
        raise NotImplementedError("Fase 1")

    async def mark_done(self, ref: CharacterRef) -> None:
        raise NotImplementedError("Fase 1")

    async def mark_failed(self, ref: CharacterRef, error: str) -> None:
        raise NotImplementedError("Fase 1")

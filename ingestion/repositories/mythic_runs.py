"""Repositório concreto de mythic runs — adapter de saída para Postgres."""

from __future__ import annotations

from collections.abc import Iterable

import asyncpg  # noqa: F401

from ingestion.domain import MythicRun


class PgMythicRunsRepo:
    def __init__(self, conn: "asyncpg.Connection") -> None:  # type: ignore[name-defined]
        self._conn = conn

    async def insert_many(self, runs: Iterable[MythicRun]) -> int:
        raise NotImplementedError("Fase 1")

    async def list_by_season(self, ref_key: str, season_slug: str) -> list[MythicRun]:
        raise NotImplementedError("Fase 1")

"""Repositório concreto de snapshots — adapter de saída para Postgres."""

from __future__ import annotations

import asyncpg  # noqa: F401

from ingestion.domain import Snapshot


class PgSnapshotsRepo:
    def __init__(self, conn: "asyncpg.Connection") -> None:  # type: ignore[name-defined]
        self._conn = conn

    async def insert(self, snapshot: Snapshot) -> None:
        raise NotImplementedError("Fase 1")

    async def latest(self, ref_key: str) -> Snapshot | None:
        raise NotImplementedError("Fase 1")

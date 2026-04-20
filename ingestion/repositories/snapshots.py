"""Repositório de snapshots. Stub da Fase 2."""

from __future__ import annotations

from typing import Protocol

from ingestion.domain import Snapshot


class SnapshotsRepo(Protocol):
    async def insert(self, snapshot: Snapshot) -> None: ...

"""Porta de saída — repositório de snapshots."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ingestion.domain import Snapshot


@runtime_checkable
class SnapshotsPort(Protocol):
    async def insert(self, snapshot: Snapshot) -> None: ...
    async def latest(self, ref_key: str) -> Snapshot | None: ...

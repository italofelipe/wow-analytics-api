"""Fake repositório de snapshots."""

from __future__ import annotations

from ingestion.domain import Snapshot


class FakeSnapshotsRepo:
    def __init__(self) -> None:
        self._store: list[Snapshot] = []

    async def insert(self, snapshot: Snapshot) -> None:
        self._store.append(snapshot)

    async def latest(self, ref_key: str) -> Snapshot | None:
        matching = [s for s in self._store if s.character_ref.key == ref_key]
        return matching[-1] if matching else None

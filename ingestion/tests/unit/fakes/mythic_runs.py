"""Fake repositório de mythic runs."""

from __future__ import annotations

from collections.abc import Iterable

from ingestion.domain import MythicRun


class FakeMythicRunsRepo:
    def __init__(self) -> None:
        self._store: list[MythicRun] = []

    async def insert_many(self, runs: Iterable[MythicRun]) -> int:
        batch = list(runs)
        self._store.extend(batch)
        return len(batch)

    async def list_by_season(self, ref_key: str, season_slug: str) -> list[MythicRun]:
        return [
            r for r in self._store
            if r.character_ref.key == ref_key and r.season_slug == season_slug
        ]

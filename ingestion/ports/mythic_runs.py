"""Porta de saída — repositório de mythic runs."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from ingestion.domain import MythicRun


@runtime_checkable
class MythicRunsPort(Protocol):
    async def insert_many(self, runs: Iterable[MythicRun]) -> int: ...
    async def list_by_season(self, ref_key: str, season_slug: str) -> list[MythicRun]: ...

"""Repositório de mythic runs. Stub da Fase 2."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from ingestion.domain import MythicRun


class MythicRunsRepo(Protocol):
    async def insert_many(self, runs: Iterable[MythicRun]) -> int: ...

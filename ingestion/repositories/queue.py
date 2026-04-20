"""Discovery queue repository. Stub da Fase 1."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from ingestion.domain import CharacterRef


class DiscoveryQueueRepo(Protocol):
    async def enqueue_many(self, refs: Iterable[CharacterRef], priority: int = 0) -> int: ...
    async def next_batch(self, limit: int) -> list[CharacterRef]: ...
    async def mark_fetched(self, ref: CharacterRef, *, error: str | None = None) -> None: ...

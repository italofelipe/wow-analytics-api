"""Porta de saída — fila de discovery."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from ingestion.domain import CharacterRef


@runtime_checkable
class DiscoveryQueuePort(Protocol):
    async def enqueue_many(self, refs: Iterable[CharacterRef], priority: int = 0) -> int: ...
    async def next_batch(self, limit: int) -> list[CharacterRef]: ...
    async def mark_done(self, ref: CharacterRef) -> None: ...
    async def mark_failed(self, ref: CharacterRef, error: str) -> None: ...

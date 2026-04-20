"""Fake fila de discovery."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from ingestion.domain import CharacterRef


class FakeDiscoveryQueueRepo:
    def __init__(self) -> None:
        self._queue: deque[CharacterRef] = deque()
        self.done: list[CharacterRef] = []
        self.failed: list[tuple[CharacterRef, str]] = []

    async def enqueue_many(self, refs: Iterable[CharacterRef], priority: int = 0) -> int:
        batch = list(refs)
        self._queue.extendleft(reversed(batch))
        return len(batch)

    async def next_batch(self, limit: int) -> list[CharacterRef]:
        result = []
        for _ in range(min(limit, len(self._queue))):
            result.append(self._queue.popleft())
        return result

    async def mark_done(self, ref: CharacterRef) -> None:
        self.done.append(ref)

    async def mark_failed(self, ref: CharacterRef, error: str) -> None:
        self.failed.append((ref, error))

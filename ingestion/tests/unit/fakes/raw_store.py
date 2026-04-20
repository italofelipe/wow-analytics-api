"""Fake raw store (substitui Cloudflare R2)."""

from __future__ import annotations

from typing import Any


class FakeRawStore:
    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    async def put_json(self, key: str, obj: dict[str, Any]) -> str:
        self._store[key] = obj
        return key

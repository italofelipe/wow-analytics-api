"""Wrapper fino do R2 (S3-compat). Stub da Fase 2.

Layout de chaves: raw/{region}/{realm}/{name}/{YYYY-MM-DD-HH}/{collector}.json
"""

from __future__ import annotations

from typing import Any, Protocol


class RawStore(Protocol):
    async def put_json(self, key: str, obj: dict[str, Any]) -> None: ...

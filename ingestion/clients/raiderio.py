"""Raider.IO client (stub — Fase 2 implementa de verdade)."""

from __future__ import annotations

from typing import Any

from ingestion.clients.base import RateLimiter


class RaiderIOClient:
    """Stub. Endpoint público, sem auth, só User-Agent identificável."""

    def __init__(
        self,
        *,
        base_url: str,
        user_agent: str,
        limiter: RateLimiter,
    ) -> None:
        self._base_url = base_url
        self._user_agent = user_agent
        self._limiter = limiter

    async def aclose(self) -> None:
        return None

    async def get_character(
        self, region: str, realm_slug: str, name: str, fields: list[str]
    ) -> dict[str, Any]:
        raise NotImplementedError("Fase 2")

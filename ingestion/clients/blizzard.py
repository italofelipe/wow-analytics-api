"""Blizzard Battle.net API client (stub — Fase 1 implementa de verdade)."""

from __future__ import annotations

from typing import Any

from ingestion.clients.base import RateLimiter


class BlizzardClient:
    """Stub. Fase 1 preencherá com OAuth, retries e endpoints reais."""

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        limiter: RateLimiter,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._limiter = limiter

    async def aclose(self) -> None:
        return None

    async def get_character_profile(
        self, region: str, realm_slug: str, name: str
    ) -> dict[str, Any]:
        raise NotImplementedError("Fase 1")

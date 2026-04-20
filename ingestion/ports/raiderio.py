"""Porta de saída — Raider.IO API."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ingestion.domain import CharacterRef, LeaderboardEntry, Snapshot


@runtime_checkable
class RaiderIOPort(Protocol):
    """Contrato para qualquer adapter que acesse o Raider.IO.

    Implementado por: ingestion.clients.raiderio.RaiderIOClient
    Fake para testes:  ingestion.tests.unit.fakes.raiderio.FakeRaiderIOAdapter
    """

    async def get_character_snapshot(
        self, ref: CharacterRef, season_slug: str
    ) -> Snapshot: ...

    async def get_leaderboard(
        self,
        region: str,
        class_slug: str,
        spec_slug: str,
        season_slug: str,
        limit: int = 100,
    ) -> list[LeaderboardEntry]: ...

    async def aclose(self) -> None: ...

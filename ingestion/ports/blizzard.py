"""Porta de saída — Blizzard Battle.net API."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ingestion.domain import Character, CharacterRef, MythicRun, RealmInfo, SeasonInfo


@runtime_checkable
class BlizzardPort(Protocol):
    """Contrato para qualquer adapter que acesse a Blizzard API.

    Implementado por: ingestion.clients.blizzard.BlizzardClient
    Fake para testes:  ingestion.tests.unit.fakes.blizzard.FakeBlizzardAdapter
    """

    async def get_character(
        self, ref: CharacterRef
    ) -> Character: ...

    async def get_mythic_runs(
        self, ref: CharacterRef, season_slug: str
    ) -> list[MythicRun]: ...

    async def get_realm_index(self, region: str) -> list[RealmInfo]: ...

    async def get_season_index(self, region: str) -> list[SeasonInfo]: ...

    async def aclose(self) -> None: ...

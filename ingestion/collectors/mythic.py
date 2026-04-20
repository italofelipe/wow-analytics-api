"""Mythic+ collector — rating, runs recentes. Stub da Fase 2."""

from __future__ import annotations

from ingestion.clients.blizzard import BlizzardClient
from ingestion.domain import CharacterRef, MythicRun


async def collect_mythic_runs(
    client: BlizzardClient, ref: CharacterRef
) -> list[MythicRun]:
    raise NotImplementedError("Fase 2")

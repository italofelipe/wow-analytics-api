"""Profile collector — ilvl, class/spec, guild. Stub da Fase 2."""

from __future__ import annotations

from ingestion.clients.blizzard import BlizzardClient
from ingestion.domain import Character, CharacterRef


async def collect_profile(client: BlizzardClient, ref: CharacterRef) -> Character:
    raise NotImplementedError("Fase 2")

"""PvP collector — ratings de 2v2/3v3/RBG/Solo Shuffle. Stub da Fase 2."""

from __future__ import annotations

from ingestion.clients.blizzard import BlizzardClient
from ingestion.domain import CharacterRef, Snapshot


async def collect_pvp(client: BlizzardClient, ref: CharacterRef) -> Snapshot:
    raise NotImplementedError("Fase 2")

"""Mythic+ collector — rating, runs recentes.

Depende de BlizzardPort e RaiderIOPort.
"""

from __future__ import annotations

from ingestion.domain import CharacterRef, MythicRun, Snapshot
from ingestion.ports.blizzard import BlizzardPort
from ingestion.ports.raiderio import RaiderIOPort


async def collect_mythic_snapshot(
    blizzard: BlizzardPort,
    raiderio: RaiderIOPort,
    ref: CharacterRef,
    season_slug: str,
) -> tuple[Snapshot, list[MythicRun]]:
    """Coleta rating M+ e runs da temporada, mesclando Blizzard + RaiderIO."""
    raise NotImplementedError("Fase 1")

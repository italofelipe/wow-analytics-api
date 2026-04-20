"""PvP collector — ratings de 2v2/3v3/RBG/Solo Shuffle.

Depende apenas de BlizzardPort.
"""

from __future__ import annotations

from ingestion.domain import CharacterRef, Snapshot
from ingestion.ports.blizzard import BlizzardPort


async def collect_pvp(blizzard: BlizzardPort, ref: CharacterRef) -> Snapshot:
    """Coleta ratings PvP atuais do personagem."""
    raise NotImplementedError("Fase 1")

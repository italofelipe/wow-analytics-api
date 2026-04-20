"""Domain models — pydantic puro, sem I/O.

Collectors retornam objetos daqui; repositories aceitam/retornam daqui.
Nenhum import de httpx, asyncpg ou aioboto3 neste subpacote.
"""

from ingestion.domain.models import (
    Character,
    CharacterRef,
    Faction,
    IngestionRun,
    LeaderboardEntry,
    MythicRun,
    PipelineStatus,
    RealmInfo,
    Region,
    SeasonInfo,
    Snapshot,
)

__all__ = [
    "Character",
    "CharacterRef",
    "Faction",
    "IngestionRun",
    "LeaderboardEntry",
    "MythicRun",
    "PipelineStatus",
    "RealmInfo",
    "Region",
    "SeasonInfo",
    "Snapshot",
]

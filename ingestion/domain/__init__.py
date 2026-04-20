"""Domain models — dataclasses/pydantic puros, sem I/O.

Collectors retornam objetos daqui; repositories aceitam/retornam daqui.
Nenhum import de httpx, asyncpg ou aioboto3 neste subpacote.
"""

from ingestion.domain.models import Character, CharacterRef, MythicRun, Snapshot

__all__ = ["Character", "CharacterRef", "MythicRun", "Snapshot"]

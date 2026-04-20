"""Ports (contratos) da arquitetura hexagonal.

Cada porta é um Protocol runtime_checkable. Adapters (clients/ e repositories/)
implementam as portas sem herdar delas — duck typing puro.

Hierarquia:
  ports/   ← contratos (este pacote)
  clients/ ← adapters de saída HTTP (implementam BlizzardPort, RaiderIOPort)
  repositories/ ← adapters de saída DB/R2 (implementam *Port de storage)
  collectors/   ← application services (dependem apenas de ports/)
"""

from ingestion.ports.blizzard import BlizzardPort
from ingestion.ports.characters import CharactersPort
from ingestion.ports.discovery_queue import DiscoveryQueuePort
from ingestion.ports.ingestion_runs import IngestionRunsPort
from ingestion.ports.mythic_runs import MythicRunsPort
from ingestion.ports.raiderio import RaiderIOPort
from ingestion.ports.raw_store import RawStorePort
from ingestion.ports.snapshots import SnapshotsPort

__all__ = [
    "BlizzardPort",
    "CharactersPort",
    "DiscoveryQueuePort",
    "IngestionRunsPort",
    "MythicRunsPort",
    "RaiderIOPort",
    "RawStorePort",
    "SnapshotsPort",
]

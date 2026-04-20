"""Fake adapters — implementações in-memory dos ports para testes unitários.

Use estes fakes em vez de mocks quando quiser comportamento real mas sem I/O:
  - Sem httpx, asyncpg ou aioboto3
  - Estado visível (inspecionável nos asserts)
  - Resetável por test fixture

Exemplo de uso:
    blizzard = FakeBlizzardAdapter()
    blizzard.seed_character(ref, character)
    collector = ProfileCollector(blizzard=blizzard)
    result = await collector.collect(ref)
    assert result == character
"""

from ingestion.tests.unit.fakes.blizzard import FakeBlizzardAdapter
from ingestion.tests.unit.fakes.characters import FakeCharactersRepo
from ingestion.tests.unit.fakes.discovery_queue import FakeDiscoveryQueueRepo
from ingestion.tests.unit.fakes.ingestion_runs import FakeIngestionRunsRepo
from ingestion.tests.unit.fakes.mythic_runs import FakeMythicRunsRepo
from ingestion.tests.unit.fakes.raiderio import FakeRaiderIOAdapter
from ingestion.tests.unit.fakes.raw_store import FakeRawStore
from ingestion.tests.unit.fakes.snapshots import FakeSnapshotsRepo

__all__ = [
    "FakeBlizzardAdapter",
    "FakeCharactersRepo",
    "FakeDiscoveryQueueRepo",
    "FakeIngestionRunsRepo",
    "FakeMythicRunsRepo",
    "FakeRaiderIOAdapter",
    "FakeRawStore",
    "FakeSnapshotsRepo",
]

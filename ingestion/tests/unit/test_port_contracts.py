"""Testes de contrato dos ports — verifica que cada fake satisfaz seu Protocol.

Se um fake não implementar todos os métodos do port correspondente, este teste
falha com um TypeError claro, antes de qualquer teste de comportamento.

Filosofia TDD: estes testes definem o contrato; os fakes são os primeiros
"adapters" que provam que o contrato é implementável.
"""

from __future__ import annotations

import pytest

from ingestion.ports import (
    BlizzardPort,
    CharactersPort,
    DiscoveryQueuePort,
    IngestionRunsPort,
    MythicRunsPort,
    RaiderIOPort,
    RawStorePort,
    SnapshotsPort,
)
from ingestion.tests.unit.fakes import (
    FakeBlizzardAdapter,
    FakeCharactersRepo,
    FakeDiscoveryQueueRepo,
    FakeIngestionRunsRepo,
    FakeMythicRunsRepo,
    FakeRaiderIOAdapter,
    FakeRawStore,
    FakeSnapshotsRepo,
)


# ── Structural contract checks (isinstance via runtime_checkable) ────────────

def test_fake_blizzard_satisfies_blizzard_port() -> None:
    assert isinstance(FakeBlizzardAdapter(), BlizzardPort)


def test_fake_raiderio_satisfies_raiderio_port() -> None:
    assert isinstance(FakeRaiderIOAdapter(), RaiderIOPort)


def test_fake_characters_repo_satisfies_characters_port() -> None:
    assert isinstance(FakeCharactersRepo(), CharactersPort)


def test_fake_snapshots_repo_satisfies_snapshots_port() -> None:
    assert isinstance(FakeSnapshotsRepo(), SnapshotsPort)


def test_fake_mythic_runs_repo_satisfies_mythic_runs_port() -> None:
    assert isinstance(FakeMythicRunsRepo(), MythicRunsPort)


def test_fake_discovery_queue_satisfies_discovery_queue_port() -> None:
    assert isinstance(FakeDiscoveryQueueRepo(), DiscoveryQueuePort)


def test_fake_raw_store_satisfies_raw_store_port() -> None:
    assert isinstance(FakeRawStore(), RawStorePort)


def test_fake_ingestion_runs_satisfies_ingestion_runs_port() -> None:
    assert isinstance(FakeIngestionRunsRepo(), IngestionRunsPort)


# ── Behavioural contract checks (smoke — fakes funcionam como esperado) ──────

@pytest.mark.asyncio
async def test_fake_characters_repo_upsert_and_find() -> None:
    from datetime import UTC, datetime
    from ingestion.domain import Character, CharacterRef

    repo = FakeCharactersRepo()
    ref = CharacterRef(region="us", realm_slug="azralon", name="Arthas")
    char = Character(ref=ref, class_slug="death-knight", level=70)

    await repo.upsert(char)
    found = await repo.find(ref)
    assert found == char


@pytest.mark.asyncio
async def test_fake_discovery_queue_enqueue_and_drain() -> None:
    from ingestion.domain import CharacterRef

    queue = FakeDiscoveryQueueRepo()
    refs = [
        CharacterRef(region="us", realm_slug="azralon", name=f"Char{i}")
        for i in range(5)
    ]

    count = await queue.enqueue_many(refs)
    assert count == 5

    batch = await queue.next_batch(limit=3)
    assert len(batch) == 3

    await queue.mark_done(batch[0])
    await queue.mark_failed(batch[1], error="timeout")

    assert len(queue.done) == 1
    assert len(queue.failed) == 1
    assert queue.failed[0][1] == "timeout"


@pytest.mark.asyncio
async def test_fake_blizzard_raises_on_unseeded_character() -> None:
    from ingestion.domain import CharacterRef

    adapter = FakeBlizzardAdapter()
    ref = CharacterRef(region="us", realm_slug="x", name="nobody")

    with pytest.raises(KeyError, match="no character seeded"):
        await adapter.get_character(ref)


@pytest.mark.asyncio
async def test_fake_ingestion_runs_full_lifecycle() -> None:
    from ingestion.domain import PipelineStatus

    repo = FakeIngestionRunsRepo()
    run = await repo.start("run_discovery")

    assert run.status == PipelineStatus.RUNNING
    assert run.finished_at is None

    finished = await repo.finish(run, PipelineStatus.SUCCESS, processed=42, errors=1)
    assert finished.status == PipelineStatus.SUCCESS
    assert finished.processed == 42
    assert finished.finished_at is not None

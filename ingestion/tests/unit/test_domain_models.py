"""Sanity checks do domínio. Mantém CI verde antes da Fase 1."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from ingestion.domain import Character, CharacterRef, MythicRun, Snapshot


def test_character_ref_key_lowercases_name() -> None:
    ref = CharacterRef(region="us", realm_slug="area-52", name="TestChar")
    assert ref.key == "us:area-52:testchar"


def test_character_ref_rejects_invalid_region() -> None:
    with pytest.raises(ValidationError):
        CharacterRef(region="br", realm_slug="x", name="y")  # type: ignore[arg-type]


def test_character_level_bounds() -> None:
    ref = CharacterRef(region="us", realm_slug="x", name="y")
    with pytest.raises(ValidationError):
        Character(ref=ref, class_slug="warrior", level=0)


def test_snapshot_tolerates_missing_optional_fields() -> None:
    ref = CharacterRef(region="eu", realm_slug="silvermoon", name="z")
    snap = Snapshot(character_ref=ref, snapshot_at=datetime.now(UTC))
    assert snap.mythic_rating is None


def test_mythic_run_requires_positive_keystone() -> None:
    ref = CharacterRef(region="us", realm_slug="x", name="y")
    with pytest.raises(ValidationError):
        MythicRun(
            run_id="r1",
            character_ref=ref,
            season_slug="tww-s2",
            dungeon_id=1,
            dungeon_slug="d",
            keystone_level=-1,
            completed_at=datetime.now(UTC),
            duration_ms=0,
            in_time=False,
        )

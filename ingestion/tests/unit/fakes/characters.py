"""Fake repositório de personagens."""

from __future__ import annotations

from ingestion.domain import Character, CharacterRef


class FakeCharactersRepo:
    def __init__(self) -> None:
        self._store: dict[str, Character] = {}

    async def upsert(self, character: Character) -> None:
        self._store[character.ref.key] = character

    async def find(self, ref: CharacterRef) -> Character | None:
        return self._store.get(ref.key)

    async def list_for_snapshot(self, limit: int = 500) -> list[CharacterRef]:
        return [c.ref for c in list(self._store.values())[:limit]]

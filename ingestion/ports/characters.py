"""Porta de saída — repositório de personagens."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ingestion.domain import Character, CharacterRef


@runtime_checkable
class CharactersPort(Protocol):
    async def upsert(self, character: Character) -> None: ...
    async def find(self, ref: CharacterRef) -> Character | None: ...
    async def list_for_snapshot(self, limit: int = 500) -> list[CharacterRef]: ...

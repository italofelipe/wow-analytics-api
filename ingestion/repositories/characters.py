"""Repositório de personagens. Stub da Fase 1."""

from __future__ import annotations

from typing import Protocol

from ingestion.domain import Character, CharacterRef


class CharactersRepo(Protocol):
    async def upsert(self, character: Character) -> None: ...
    async def find(self, ref: CharacterRef) -> Character | None: ...

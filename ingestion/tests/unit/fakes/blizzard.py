"""Fake adapter da Blizzard API — sem HTTP real."""

from __future__ import annotations

from ingestion.domain import Character, CharacterRef, MythicRun, RealmInfo, SeasonInfo


class FakeBlizzardAdapter:
    """In-memory double de BlizzardPort.

    Seed via `seed_character()`, `seed_runs()`, etc.
    Inspecione `calls` para verificar quais métodos foram chamados.
    """

    def __init__(self) -> None:
        self._characters: dict[str, Character] = {}
        self._runs: dict[str, list[MythicRun]] = {}
        self._realms: dict[str, list[RealmInfo]] = {}
        self._seasons: dict[str, list[SeasonInfo]] = {}
        self.calls: list[tuple[str, object]] = []

    # ── Seed helpers ────────────────────────────────────────────

    def seed_character(self, character: Character) -> None:
        self._characters[character.ref.key] = character

    def seed_runs(self, ref: CharacterRef, season_slug: str, runs: list[MythicRun]) -> None:
        self._runs[f"{ref.key}:{season_slug}"] = runs

    def seed_realms(self, region: str, realms: list[RealmInfo]) -> None:
        self._realms[region] = realms

    def seed_seasons(self, region: str, seasons: list[SeasonInfo]) -> None:
        self._seasons[region] = seasons

    # ── BlizzardPort interface ───────────────────────────────────

    async def get_character(self, ref: CharacterRef) -> Character:
        self.calls.append(("get_character", ref))
        if ref.key not in self._characters:
            raise KeyError(f"FakeBlizzardAdapter: no character seeded for {ref.key!r}")
        return self._characters[ref.key]

    async def get_mythic_runs(self, ref: CharacterRef, season_slug: str) -> list[MythicRun]:
        self.calls.append(("get_mythic_runs", (ref, season_slug)))
        return self._runs.get(f"{ref.key}:{season_slug}", [])

    async def get_realm_index(self, region: str) -> list[RealmInfo]:
        self.calls.append(("get_realm_index", region))
        return self._realms.get(region, [])

    async def get_season_index(self, region: str) -> list[SeasonInfo]:
        self.calls.append(("get_season_index", region))
        return self._seasons.get(region, [])

    async def aclose(self) -> None:
        pass

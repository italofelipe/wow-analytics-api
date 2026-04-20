"""Fake adapter do Raider.IO — sem HTTP real."""

from __future__ import annotations

from ingestion.domain import CharacterRef, LeaderboardEntry, Snapshot


class FakeRaiderIOAdapter:
    def __init__(self) -> None:
        self._snapshots: dict[str, Snapshot] = {}
        self._leaderboards: dict[str, list[LeaderboardEntry]] = {}
        self.calls: list[tuple[str, object]] = []

    def seed_snapshot(self, snapshot: Snapshot) -> None:
        self._snapshots[snapshot.character_ref.key] = snapshot

    def seed_leaderboard(
        self,
        region: str,
        class_slug: str,
        spec_slug: str,
        season_slug: str,
        entries: list[LeaderboardEntry],
    ) -> None:
        key = f"{region}:{class_slug}:{spec_slug}:{season_slug}"
        self._leaderboards[key] = entries

    async def get_character_snapshot(self, ref: CharacterRef, season_slug: str) -> Snapshot:
        self.calls.append(("get_character_snapshot", (ref, season_slug)))
        if ref.key not in self._snapshots:
            raise KeyError(f"FakeRaiderIOAdapter: no snapshot seeded for {ref.key!r}")
        return self._snapshots[ref.key]

    async def get_leaderboard(
        self,
        region: str,
        class_slug: str,
        spec_slug: str,
        season_slug: str,
        limit: int = 100,
    ) -> list[LeaderboardEntry]:
        key = f"{region}:{class_slug}:{spec_slug}:{season_slug}"
        self.calls.append(("get_leaderboard", key))
        return self._leaderboards.get(key, [])[:limit]

    async def aclose(self) -> None:
        pass

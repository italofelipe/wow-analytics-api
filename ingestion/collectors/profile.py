"""Profile collector — ilvl, class/spec, guild.

Depende de BlizzardPort (não de BlizzardClient diretamente).
Testável com FakeBlizzardAdapter sem HTTP real.
"""

from __future__ import annotations

from ingestion.domain import Character, CharacterRef
from ingestion.ports.blizzard import BlizzardPort


async def collect_profile(blizzard: BlizzardPort, ref: CharacterRef) -> Character:
    """Busca o perfil completo de um personagem via Blizzard API."""
    raise NotImplementedError("Fase 1")

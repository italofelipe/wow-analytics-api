"""Domínio tipado.

Regras:
- Imutáveis (pydantic `frozen=True`) pra evitar mutação acidental entre camadas.
- Sem dependências de I/O.
- Naming: `Ref` = identificador, `Model` completo = objeto de leitura,
  novos campos entram opcionais quando a fonte pode não ter.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


Region = Literal["us", "eu", "kr", "tw"]
Faction = Literal["alliance", "horde", "neutral"]


class CharacterRef(_Frozen):
    """Identificador mínimo e estável de um personagem.

    Chave natural é (region, realm_slug, name) lowercase.
    """

    region: Region
    realm_slug: str
    name: str

    @property
    def key(self) -> str:
        return f"{self.region}:{self.realm_slug}:{self.name.lower()}"


class Character(_Frozen):
    ref: CharacterRef
    class_slug: str
    race: str | None = None
    faction: Faction | None = None
    gender: str | None = None
    level: int = Field(ge=1, le=200)
    guild: str | None = None


class Snapshot(_Frozen):
    character_ref: CharacterRef
    snapshot_at: datetime
    season_slug: str | None = None
    item_level_equipped: float | None = None
    item_level_avg: float | None = None
    spec_active: str | None = None
    mythic_rating: float | None = None
    mythic_rating_color: str | None = None
    pvp_2v2: int | None = None
    pvp_3v3: int | None = None
    pvp_solo_shuffle: int | None = None
    pvp_rbg: int | None = None
    honor_level: int | None = None
    achievements_pts: int | None = None
    raw_r2_key: str | None = None


class MythicRun(_Frozen):
    run_id: str
    character_ref: CharacterRef
    season_slug: str
    dungeon_id: int
    dungeon_slug: str
    keystone_level: int = Field(ge=0)
    completed_at: datetime
    duration_ms: int = Field(ge=0)
    in_time: bool
    score: float | None = None

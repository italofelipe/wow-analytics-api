"""Domínio tipado.

Regras:
- Imutáveis (pydantic `frozen=True`) pra evitar mutação acidental entre camadas.
- Sem dependências de I/O.
- Naming: `Ref` = identificador, model completo = objeto de leitura.
  Novos campos entram opcionais quando a fonte pode não ter.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


Region = Literal["us", "eu", "kr", "tw"]
Faction = Literal["alliance", "horde", "neutral"]


# ─── Core domain ─────────────────────────────────────────────────────────────

class CharacterRef(_Frozen):
    """Identificador mínimo e estável de um personagem.

    Chave natural: (region, realm_slug, name) lowercase.
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


# ─── Supporting domain types (used by ports) ─────────────────────────────────

class RealmInfo(_Frozen):
    """Dados básicos de um realm, vindos do índice da Blizzard."""

    slug: str
    name: str
    region: Region
    locale: str = "en_US"
    is_connected: bool = True


class SeasonInfo(_Frozen):
    """Dados de uma temporada de M+, vindos da Blizzard."""

    slug: str
    name: str
    region: Region
    is_current: bool = False


class LeaderboardEntry(_Frozen):
    """Entrada de leaderboard do Raider.IO — usada pelo discovery pipeline."""

    ref: CharacterRef
    score: float = Field(ge=0)
    rank: int = Field(ge=1)
    class_slug: str
    spec_slug: str | None = None


# ─── Pipeline run tracking ────────────────────────────────────────────────────

class PipelineStatus(str, Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED  = "failed"


class IngestionRun(_Frozen):
    """Registro de uma execução de pipeline — persiste em ingestion_runs."""

    id: str
    pipeline: str
    status: PipelineStatus
    started_at: datetime
    finished_at: datetime | None = None
    processed: int = Field(default=0, ge=0)
    errors: int = Field(default=0, ge=0)
    meta: dict[str, str] = Field(default_factory=dict)

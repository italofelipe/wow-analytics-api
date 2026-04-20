"""Porta de saída — rastreamento de execuções de pipeline."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ingestion.domain import IngestionRun, PipelineStatus


@runtime_checkable
class IngestionRunsPort(Protocol):
    async def start(self, pipeline: str) -> IngestionRun: ...
    async def finish(
        self,
        run: IngestionRun,
        status: PipelineStatus,
        processed: int = 0,
        errors: int = 0,
    ) -> IngestionRun: ...

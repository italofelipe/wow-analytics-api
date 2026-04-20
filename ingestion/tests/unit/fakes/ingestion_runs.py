"""Fake rastreador de execuções de pipeline."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from ingestion.domain import IngestionRun, PipelineStatus


class FakeIngestionRunsRepo:
    def __init__(self) -> None:
        self._store: list[IngestionRun] = []

    async def start(self, pipeline: str) -> IngestionRun:
        run = IngestionRun(
            id=str(uuid.uuid4()),
            pipeline=pipeline,
            status=PipelineStatus.RUNNING,
            started_at=datetime.now(UTC),
        )
        self._store.append(run)
        return run

    async def finish(
        self,
        run: IngestionRun,
        status: PipelineStatus,
        processed: int = 0,
        errors: int = 0,
    ) -> IngestionRun:
        finished = run.model_copy(update={
            "status": status,
            "finished_at": datetime.now(UTC),
            "processed": processed,
            "errors": errors,
        })
        self._store = [finished if r.id == run.id else r for r in self._store]
        return finished

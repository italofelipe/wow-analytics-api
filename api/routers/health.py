"""Healthcheck — barato, sem DB (serve pra smoke pós-deploy)."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    from api import __version__  # noqa: PLC0415

    return HealthResponse(status="ok", version=__version__)

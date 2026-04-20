"""Smoke test do /health — não depende de DB."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import ASGITransport, AsyncClient

from api.routers import health


@pytest.fixture
def app_without_db() -> FastAPI:
    """App isolado do lifespan pra evitar conexão com Supabase nos testes unit."""
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_methods=["GET"],
    )
    app.include_router(health.router)
    return app


async def test_health_returns_ok(app_without_db: FastAPI) -> None:
    transport = ASGITransport(app=app_without_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body

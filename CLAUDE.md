# wow-analytics-api

Backend Python do WoW Analytics: FastAPI, pipelines de ingestão, migrations Supabase.

## System context

Full architecture, ADRs, API contract and runbooks are in the `context/` submodule.
Read `context/CLAUDE.md` for a complete picture of the system before making changes.

## This repo

- **Stack:** Python 3.12, `uv`, `httpx`, `tenacity`, `asyncpg`, `aioboto3`, FastAPI
- **Layer rules:** `clients → collectors → repositories → pipelines/routers` (see `context/CLAUDE.md`)
- **Test tools:** pytest, Schemathesis (contract), Newman (Postman collections), k6 (load)
- **Scheduler:** GitHub Actions cron — discovery 1×/day, snapshot 2×/day, aggregate 1×/day

## Local setup

```bash
git clone --recurse-submodules https://github.com/italofelipe/wow-analytics-api
cd wow-analytics-api
uv sync --all-extras --group dev
cp .env.example .env  # fill in BLIZZARD_CLIENT_ID, BLIZZARD_CLIENT_SECRET, DATABASE_URL
supabase start
uvicorn api.main:app --reload
```

## Layer rules (enforced in PR review)

- `ingestion/clients/`: HTTP only — no asyncpg/aioboto3 imports
- `ingestion/collectors/`: No asyncpg/aioboto3 — receives clients, returns domain dataclasses
- `ingestion/repositories/`: Only layer that touches Postgres or R2 — no httpx
- `ingestion/pipelines/` and `api/routers/`: Wiring only — instantiate and inject
- `ingestion/domain/`: Pure pydantic/stdlib — no I/O

## Running pipelines manually

```bash
uv run python -m ingestion.pipelines.run_discovery --dry-run
uv run python -m ingestion.pipelines.run_snapshot
uv run python -m ingestion.pipelines.run_aggregate
```

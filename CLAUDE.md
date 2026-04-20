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

## Architecture: Hexagonal (Ports & Adapters)

```
domain/ ←── ports/ ←── collectors/
                   ↗
clients/ / repositories/  (implement ports, do not inherit)
pipelines/ / routers/     (wiring: instantiate adapters, inject into collectors)
```

### Layer rules (enforced in PR review)

- `ingestion/ports/`: Protocol definitions only — no I/O, no business logic
- `ingestion/domain/`: Pure pydantic/stdlib — no I/O imports of any kind
- `ingestion/clients/`: HTTP adapters — implement ports, no asyncpg/aioboto3
- `ingestion/repositories/`: DB/R2 adapters — implement ports, no httpx
- `ingestion/collectors/`: Application services — import only from `ports/` and `domain/`
- `ingestion/pipelines/` and `api/routers/`: Wiring only — instantiate and inject

### TDD workflow

1. Write test using `FakeXxxAdapter` from `tests/unit/fakes/`
2. Test fails (NotImplementedError) — implement the collector
3. Test passes — implement the real adapter (client or repository)
4. Integration test verifies the real adapter against Supabase local

### Fakes

All ports have in-memory fake implementations in `ingestion/tests/unit/fakes/`.
`test_port_contracts.py` asserts `isinstance(fake, Port)` for every pair.

## Running pipelines manually

```bash
uv run python -m ingestion.pipelines.run_discovery --dry-run
uv run python -m ingestion.pipelines.run_snapshot
uv run python -m ingestion.pipelines.run_aggregate
```

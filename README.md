# WoW Analytics

Ingestão, modelagem e análise de dados de World of Warcraft. Puxa métricas de
personagens (M+, PvP, ilvl, progressão) via APIs públicas, normaliza em
Postgres e serve um dashboard Nuxt.

**Status:** em construção (Fase 0 — fundações).

## Arquitetura

Ver [`docs/architecture.md`](docs/architecture.md) para diagrama e princípios.

Resumo:

- **Ingestão** (Python 3.12 + `httpx` async) roda em GitHub Actions (cron 2x/dia).
- **Raw JSON** em Cloudflare R2 (10 GB free, lifecycle de 30 dias).
- **Normalizado** em Supabase Postgres (500 MB free).
- **API** em FastAPI (Vercel Python Serverless).
- **Front** em Nuxt 3 + Vue 3 + TypeScript strict (Vercel).
- **Contrato** API ↔ front gerado via `openapi-typescript` — type-safety end-to-end.

## Pré-requisitos

| Ferramenta | Versão mínima | Como instalar |
|---|---|---|
| Python | 3.12 | <https://www.python.org/downloads/> |
| uv | 0.5+ | `curl -LsSf https://astral.sh/uv/install.sh \| sh` (unix) ou `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` (win) |
| Node | 20+ | <https://nodejs.org/> |
| pnpm | 9+ | `corepack enable && corepack prepare pnpm@latest --activate` |
| Supabase CLI | 1.200+ | `npm i -g supabase` ou <https://supabase.com/docs/guides/cli> |
| Docker | 24+ | obrigatório para `supabase start` (DB local) |

## Setup local

```bash
# 1. Clonar e entrar no repo
git clone <url> && cd wow_analytics

# 2. Copiar template de env e preencher credenciais
cp .env.example .env

# 3. Instalar dependências Python (cria .venv automático)
uv sync --all-extras

# 4. Instalar dependências web
cd web && pnpm install && cd ..

# 5. Subir Supabase local (Postgres + Studio em http://localhost:54323)
supabase start

# 6. Aplicar migrations
supabase db reset   # reseta e reaplica tudo em supabase/migrations/

# 7. Instalar hooks do pre-commit
uv run pre-commit install
```

## Rodar localmente

### Pipelines de ingestão

```bash
# Descobrir personagens (lê leaderboards de M+ e popula discovery_queue)
uv run python -m ingestion.pipelines.run_discovery --region us --realm-limit 3

# Snapshot de métricas dos personagens na fila
uv run python -m ingestion.pipelines.run_snapshot --limit 50

# Recomputar marts (stats por classe, leaderboards)
uv run python -m ingestion.pipelines.run_aggregate
```

### API

```bash
uv run uvicorn api.main:app --reload --port 8000
# OpenAPI: http://localhost:8000/docs
```

### Front

```bash
cd web && pnpm dev
# http://localhost:3000
```

### Tipos da API (rodar sempre que mudar o schema)

```bash
bash scripts/generate-api-types.sh
```

## Testes

```bash
# Python
uv run pytest

# Web unit
cd web && pnpm test

# Web e2e (precisa de API + front rodando)
cd web && pnpm exec playwright test
```

## Deploy

- **API + front**: `git push origin main` → Vercel faz auto-deploy.
- **Cron jobs**: rodam sozinhos via GitHub Actions (ver `.github/workflows/`).
- **Migrations**: `supabase db push --linked` após `supabase link`.

## Estrutura

```
ingestion/   # coletores assíncronos (clients → collectors → repositories → pipelines)
api/         # FastAPI read layer
web/         # Nuxt 3 + Vue 3
supabase/    # migrations versionadas
docs/        # arquitetura e runbooks
scripts/     # utilitários (geração de tipos etc.)
.github/     # CI + cron jobs
```

## Licença

MIT (a definir).

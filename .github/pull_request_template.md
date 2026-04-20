## O que muda

<!-- Em 1–2 frases: o que esse PR entrega. -->

## Por quê

<!-- Motivação / link pra issue ou decisão. -->

## Como testar

- [ ] `uv run pytest`
- [ ] `cd web && pnpm test`
- [ ] Smoke manual:

## Checklist

- [ ] `ruff`, `mypy`, `vue-tsc` verdes localmente
- [ ] Se mexeu em endpoint / schema: rodei `bash scripts/generate-api-types.sh`
- [ ] Se mexeu em schema do DB: criei migration via `bash scripts/new-migration.sh`
- [ ] Atualizei `docs/` se mudou comportamento visível

## Observações

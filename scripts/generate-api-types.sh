#!/usr/bin/env bash
# Gera web/types/api.d.ts a partir do schema OpenAPI da FastAPI.
#
# Uso:
#   bash scripts/generate-api-types.sh              # escreve/atualiza o arquivo
#   bash scripts/generate-api-types.sh --check      # falha se o arquivo estiver dessincronizado (usado no CI)
#
# Requisitos: `uv` e `pnpm`/`npx` no PATH.
# A API pode estar rodando local (uvicorn) OU o schema pode ser extraído offline
# importando o app. O modo offline é preferido no CI — zero dependência de rede.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

MODE="write"
if [[ "${1:-}" == "--check" ]]; then
    MODE="check"
fi

OUT_FILE="web/types/api.d.ts"
TMP_SCHEMA="$(mktemp -t wow-openapi-XXXXXX.json)"
trap 'rm -f "$TMP_SCHEMA"' EXIT

echo "→ extraindo schema OpenAPI do app FastAPI…"
uv run python -c "import json; from api.main import app; print(json.dumps(app.openapi()))" > "$TMP_SCHEMA"

echo "→ gerando tipos TypeScript…"
mkdir -p "$(dirname "$OUT_FILE")"
NEW_CONTENT="$(npx --yes openapi-typescript@7 "$TMP_SCHEMA")"

if [[ "$MODE" == "check" ]]; then
    if [[ ! -f "$OUT_FILE" ]]; then
        echo "✗ $OUT_FILE não existe — rode sem --check para gerar." >&2
        exit 1
    fi
    if ! diff -q <(printf '%s\n' "$NEW_CONTENT") "$OUT_FILE" > /dev/null; then
        echo "✗ $OUT_FILE dessincronizado do schema OpenAPI." >&2
        echo "  Rode: bash scripts/generate-api-types.sh" >&2
        diff -u "$OUT_FILE" <(printf '%s\n' "$NEW_CONTENT") || true
        exit 1
    fi
    echo "✓ tipos sincronizados."
else
    printf '%s\n' "$NEW_CONTENT" > "$OUT_FILE"
    echo "✓ $OUT_FILE atualizado."
fi

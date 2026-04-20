#!/usr/bin/env bash
# Wrapper sobre `supabase migration new` com convenção de nome consistente.
#
# Uso:
#   bash scripts/new-migration.sh <snake_case_name>
#
# Gera: supabase/migrations/<YYYYMMDDHHMMSS>_<name>.sql

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "uso: $0 <snake_case_name>" >&2
    exit 2
fi

NAME="$1"
if [[ ! "$NAME" =~ ^[a-z][a-z0-9_]*$ ]]; then
    echo "✗ nome inválido: '$NAME' — use snake_case lower." >&2
    exit 2
fi

exec supabase migration new "$NAME"

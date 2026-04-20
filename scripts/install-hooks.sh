#!/usr/bin/env bash
# Install all local dev hooks for wow-analytics-api.
# Run once after cloning: ./scripts/install-hooks.sh

set -euo pipefail

echo "==> Checking prerequisites..."

if ! command -v uv &>/dev/null; then
  echo "ERROR: uv not found. Install from https://docs.astral.sh/uv/getting-started/installation/"
  exit 1
fi

if ! command -v pre-commit &>/dev/null; then
  echo "==> Installing pre-commit via uv..."
  uv tool install pre-commit
fi

# Install gitleaks if not present
if ! command -v gitleaks &>/dev/null; then
  echo "==> gitleaks not found — installing via pre-commit hooks (will be downloaded on first run)"
  echo "    Alternatively: https://github.com/gitleaks/gitleaks#installing"
fi

echo "==> Installing pre-commit hooks..."
pre-commit install                        # pre-commit hook
pre-commit install --hook-type pre-push   # pre-push hook

echo "==> Running hooks on all files (first-time check)..."
pre-commit run --all-files || true

echo ""
echo "✓ Hooks installed. Summary:"
echo "  pre-commit : gitleaks, ruff lint+format, detect-private-key"
echo "  pre-push   : mypy, bandit, pytest unit tests"
echo "  manual     : openapi-types-drift (run with: pre-commit run openapi-types-drift --hook-stage manual)"

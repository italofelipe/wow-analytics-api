"""Discovery pipeline: varre leaderboards de M+ e popula discovery_queue.

Stub da Fase 1. Mantemos o módulo com `main()` importável pra CI validar
que o skeleton carrega sem explodir.
"""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    _ = argv
    print("run_discovery: not implemented yet (Fase 1)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

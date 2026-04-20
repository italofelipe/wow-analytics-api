"""Snapshot pipeline: consome discovery_queue e grava snapshots em PG + R2.

Stub da Fase 2.
"""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    _ = argv
    print("run_snapshot: not implemented yet (Fase 2)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

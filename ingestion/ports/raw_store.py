"""Porta de saída — armazenamento de JSON bruto (Cloudflare R2)."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class RawStorePort(Protocol):
    async def put_json(self, key: str, obj: dict[str, Any]) -> str: ...
    # Retorna a chave S3 do objeto gravado.

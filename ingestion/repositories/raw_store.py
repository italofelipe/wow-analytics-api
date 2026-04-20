"""Raw store concreto — adapter de saída para Cloudflare R2 (S3-compat).

Layout de chaves: raw/{region}/{realm}/{name}/{YYYY-MM-DD-HH}/{collector}.json
"""

from __future__ import annotations

from typing import Any

import aioboto3  # noqa: F401


class R2RawStore:
    def __init__(self, bucket: str, session: "aioboto3.Session") -> None:  # type: ignore[name-defined]
        self._bucket = bucket
        self._session = session

    async def put_json(self, key: str, obj: dict[str, Any]) -> str:
        raise NotImplementedError("Fase 1")

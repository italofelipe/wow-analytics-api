# syntax=docker/dockerfile:1
# Multi-stage build: builder instala deps, runtime é imagem mínima.

FROM python:3.12-slim AS builder

RUN pip install uv
WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv sync --extra api --no-dev --frozen

COPY api/ ./api/
COPY ingestion/ ./ingestion/

# ─────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

RUN useradd --no-create-home --shell /bin/false app
WORKDIR /app

COPY --from=builder /app /app
COPY --from=builder /root/.local /root/.local

ENV PATH="/root/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

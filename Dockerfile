# PrecisionRx prototype — one image: Astro UI (built) + FastAPI (engines, API, CDS Hooks). Synthetic data only.

# ---- 1. build the Astro site
FROM node:22-slim AS web
RUN corepack enable
WORKDIR /web
COPY web/package.json web/pnpm-lock.yaml web/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
COPY web/ ./
RUN pnpm build

# ---- 2. Python runtime
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
COPY app/ app/
COPY data/ data/
COPY eval/ eval/
COPY --from=web /web/dist web/dist
RUN uv run python -m eval.run_eval >/dev/null
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "uv run --no-sync uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]

FROM python:3.11-slim

RUN set -eux; \
    apt-get update -yqq; \
    apt-get install -y \
      spatialite-bin \
      libsqlite3-mod-spatialite \
      gdal-bin

COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /uvx /bin/

COPY . /app/

WORKDIR /app/

RUN uv sync --locked

FROM python:3.11-slim

RUN set -eux; \
    apt-get update -yqq; \
    apt-get install -y \
      spatialite-bin \
      libsqlite3-mod-spatialite \
      gdal-bin

COPY . /app/

WORKDIR /app/

RUN pip install --upgrade -r requirements.txt -r requirements_dev.txt

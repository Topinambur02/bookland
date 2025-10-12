FROM python:3.13-alpine

RUN apk add --no-cache curl

RUN apk add --no-cache --virtual .build-deps \
    build-base \
    libffi-dev \
    && pip install --no-cache-dir poetry==1.8.0 \
    && apk del .build-deps

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry"

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry install --no-root

COPY . /app
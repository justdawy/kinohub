FROM python:3.14.4-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --locked --no-dev

COPY . /app

EXPOSE 8000

CMD ["uv", "run", "kinohub/manage.py", "runserver", "0.0.0.0:8000"]

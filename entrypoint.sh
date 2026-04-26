#!/bin/sh

set -e

echo "Waiting for Postgres..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Postgres is up - running migrations..."

uv run kinohub/manage.py migrate --noinput

echo "Starting Django server..."

uv run kinohub/manage.py runserver 0.0.0.0:8000

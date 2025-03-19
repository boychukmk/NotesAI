#!/bin/bash

set -e

echo "Waiting for Postgres ..."
until pg_isready -h db -p 5432 -U user; do
  sleep 1
done
echo "Postgres is accessible !"

if [[ "$1" == "test" ]]; then
    echo "Running tests with coverage..."
    coverage run -m pytest --asyncio-mode=auto
    coverage report
    exit 0
fi

echo "Applying migrations Alembic..."
alembic -c /backend/app/alembic.ini upgrade head

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

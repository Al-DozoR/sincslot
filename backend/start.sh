#!/bin/sh
set -e

echo "Waiting for database..."

until alembic upgrade head; do
  echo "DB not ready, retrying..."
  sleep 2
done

echo "DB ready"

uvicorn main:app \
  --host 0.0.0.0 \
  --port 10004 \
  --reload


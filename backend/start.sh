#!/bin/sh

until alembic upgrade head
do
    echo "Waiting for db to be ready..."
    sleep 2
done
pytest . -v --cache-clear
uvicorn main:app --reload --host 0.0.0.0 --port 10004

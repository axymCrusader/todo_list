#!/bin/bash

until nc -z -v -w30 db 5432; do
  echo "Waiting for database connection..."
  sleep 1
done

if [ ! -d "alembic/versions" ]; then
  mkdir -p alembic/versions
  alembic revision --autogenerate -m "Initial migration"
fi

alembic upgrade head


exec uvicorn src.main:app --host 0.0.0.0 --port 8000

#!/bin/bash
# Development server. Does not touch the production gunicorn process.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p "${ROOT}/temp"

export CHEMMAPS_DB_CONFIG="${ROOT}/database.ini"
export CHEMMAPS_TEMP="${ROOT}/temp"

exec /home/alexb/.conda/envs/django_dev/bin/python manage.py runserver 0.0.0.0:8001 --settings=settings.local

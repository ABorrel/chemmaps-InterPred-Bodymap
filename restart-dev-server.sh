#!/usr/bin/env bash
# Restart ChemMaps Django dev server (WSL + chemmaps-dev conda env).
# Usage: bash restart-dev-server.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON="${CHEMMAPS_PYTHON:-/home/alexborrel/miniforge3/envs/chemmaps-dev/bin/python}"
PG_CTL="${CHEMMAPS_PG_CTL:-/home/alexborrel/miniforge3/envs/chemmaps-dev/bin/pg_ctl}"
PGDATA="${CHEMMAPS_PGDATA:-$HOME/pgdata-chemmaps}"
PGPORT="${CHEMMAPS_PGPORT:-5433}"
HOST="${CHEMMAPS_HOST:-0.0.0.0}"
PORT="${CHEMMAPS_PORT:-8000}"

echo "Stopping existing Django runserver processes..."
pkill -f 'manage.py runserver' 2>/dev/null || true
sleep 1

echo "Checking PostgreSQL on port ${PGPORT}..."
if ! "$PG_CTL" -D "$PGDATA" status >/dev/null 2>&1; then
    echo "Starting PostgreSQL..."
    "$PG_CTL" -D "$PGDATA" -o "-p ${PGPORT}" -l "${PGDATA}/logfile" start
else
    echo "PostgreSQL already running."
fi

echo "Starting Django at http://localhost:${PORT}/"
exec "$PYTHON" manage.py runserver "${HOST}:${PORT}" --settings=settings.local --skip-checks

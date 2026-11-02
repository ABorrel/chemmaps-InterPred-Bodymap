#!/bin/bash
# Merge VM_dev into the production checkout. Restarts gunicorn only with --restart.
# Never copies chemmaps_dev over chemmaps_local and never switches production onto django_dev.
set -euo pipefail

DEV_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROD_ROOT="/home/alexb/django_server"
PROD_INI="/home/alexb/database.ini"
PY="/home/alexb/.conda/envs/django_run/bin/python"
GUNICORN="/home/alexb/.conda/envs/django_run/bin/gunicorn"
RESTART=0
MIGRATE=0

for arg in "$@"; do
  case "$arg" in
    --restart) RESTART=1 ;;
    --migrate) MIGRATE=1 ;;
    *)
      echo "Unknown argument: $arg" >&2
      echo "Usage: $0 [--migrate] [--restart]" >&2
      exit 2
      ;;
  esac
done

cd "$DEV_ROOT"
if [[ "$(git rev-parse --abbrev-ref HEAD)" != "VM_dev" ]]; then
  echo "This script must be run from the VM_dev worktree (${DEV_ROOT})." >&2
  exit 1
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "VM_dev has uncommitted changes. Commit them before promoting." >&2
  exit 1
fi

cd "$PROD_ROOT"
if [[ "$(git rev-parse --abbrev-ref HEAD)" != "VM_prod" ]]; then
  echo "Production checkout is not on VM_prod." >&2
  exit 1
fi
if [[ -n "$(git diff --name-only)" || -n "$(git diff --cached --name-only)" ]]; then
  echo "Production checkout has tracked changes. Leave /home/alexb/django_server unchanged before promoting." >&2
  exit 1
fi

if ! git diff --quiet VM_prod...VM_dev -- settings/production.py; then
  echo "Refusing: this merge would change settings/production.py." >&2
  exit 1
fi

db_name=$(awk -F= '/^(database|dbname)=/ {gsub(/[ \t\r]/, "", $2); print $2; exit}' "$PROD_INI")
db_port=$(awk -F= '/^port=/ {gsub(/[ \t\r]/, "", $2); print $2; exit}' "$PROD_INI")
if [[ "$db_name" != "chemmaps_local" || "$db_port" != "5432" ]]; then
  echo "Refusing: ${PROD_INI} must stay database chemmaps_local on port 5432 (found ${db_name} port ${db_port})." >&2
  exit 1
fi

model_changes=$(git diff --name-only VM_prod...VM_dev | grep -E '(^|/)(models\.py|migrations/)' || true)
if [[ -n "$model_changes" && "$MIGRATE" -ne 1 ]]; then
  echo "Model or migration files differ:" >&2
  echo "$model_changes" >&2
  echo "Re-run with --migrate to apply them to chemmaps_local after the merge." >&2
  echo "  cd ${PROD_ROOT} && ${PY} manage.py migrate --settings=settings.production" >&2
  exit 1
fi

echo "Merging VM_dev into ${PROD_ROOT} (VM_prod)"
git merge --no-edit VM_dev

if [[ "$MIGRATE" -eq 1 ]]; then
  echo "Migrating chemmaps_local with settings.production"
  "$PY" manage.py migrate --settings=settings.production
fi

echo "Production still uses ${PROD_INI} and conda env django_run."
echo "Install any package added in django_dev into django_run before restarting gunicorn."
if [[ "$RESTART" -ne 1 ]]; then
  echo "Merge is in the production tree. Python code goes live when gunicorn restarts."
  echo "Restart with:"
  echo "  cd /home/alexb && ${GUNICORN} -c conf/gunicor_config_chemmaps.py django_server.wsgi --env DJANGO_SETTINGS_MODULE=settings.production"
  echo "Or re-run: $0 --restart"
  exit 0
fi

echo "Restarting the chemmaps gunicorn master only"
pkill -f 'gunicor_config_chemmaps.py' || true
sleep 2
cd /home/alexb
nohup "$GUNICORN" -c conf/gunicor_config_chemmaps.py django_server.wsgi --env DJANGO_SETTINGS_MODULE=settings.production \
  >/home/alexb/gunicorn.log 2>&1 &
echo "Gunicorn restarted from /home/alexb with django_run and settings.production."

#!/bin/bash

set -e
cmd="$@"

alias opera='/usr/local/bin/OPERA/application/run_OPERA.sh $LD_LIBRARY'

/opt/conda/envs/chemmaps/bin/python /app/project/manage.py migrate
/opt/conda/envs/chemmaps/bin/python /app/project/manage.py collectstatic --noinput

/opt/conda/envs/chemmaps/bin/gunicorn django_server.wsgi:application \
     --workers 8 \
     --timeout 90 \
     --reload \
     --bind 0.0.0.0:8001 \
     --chdir /app/project

#!/bin/bash

set -e
cmd="$@"

# Filler
# exec $cmd

/opt/conda/envs/chemmaps/bin/python /app/project/manage.py migrate
/opt/conda/envs/chemmaps/bin/python /app/project/manage.py collectstatic --noinput

/opt/conda/envs/chemmaps/bin/gunicorn django_server.wsgi:application \
     --workers 8 \
     --bind 0.0.0.0:8000 \
     --chdir /app/project

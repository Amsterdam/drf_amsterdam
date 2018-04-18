#!/usr/bin/env bash

echo "The docker-run.sh script"
set -x   # Echo all commands lines
set -u   # crash on missing env variables
set -e   # stop on any error

# collect static files
yes yes | python manage.py collectstatic

# run uwsgi
cd /app/

# Multiple static-maps cannot be passed via UWSGI_STATIC_MAP env. variable, hence:
exec uwsgi --static-map /onderwijs/dash/=/vue_static --static-map /onderwijs/static=/static

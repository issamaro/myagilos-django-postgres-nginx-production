#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --no-input
python manage.py migrate
uwsgi --socket :8000 --master --enable-threads --module agilos.wsgi
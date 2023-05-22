#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py migrate
python manage.py collectstatic --no-input
sass /vol/web/static/style.scss /vol/static/style.css
uwsgi --socket :8000 --master --enable-threads --module agilos.wsgi
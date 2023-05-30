#!/bin/sh

set -e

echo "Running wait_for_db script..." && python manage.py wait_for_db && echo "wait_for_db executed"
# echo "making migrations..." && python manage.py makemigrations
echo "trying to migrate..." && python manage.py migrate
echo "collecting static files..." && python manage.py collectstatic --no-input
echo "activating uwsgi..." && uwsgi --socket :8000 --master --enable-threads --module agilos.wsgi
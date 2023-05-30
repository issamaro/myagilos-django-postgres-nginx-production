#!/bin/sh

set -e

# wait-for-it functionality
WAITFORIT_HOST="db" # adjust to your database host
WAITFORIT_PORT=5432 # adjust to your database port
WAITFORIT_TIMEOUT=5
WAITFORIT_STRICT=0
WAITFORIT_QUIET=0

wait_for()
{
    if [ "$WAITFORIT_TIMEOUT" -gt 0 ]; then
        echo "Waiting $WAITFORIT_TIMEOUT seconds for $WAITFORIT_HOST:$WAITFORIT_PORT"
    else
        echo "Waiting for $WAITFORIT_HOST:$WAITFORIT_PORT without a timeout"
    fi
    start_ts=$(date +%s)
    while :
    do
        nc -z "$WAITFORIT_HOST" "$WAITFORIT_PORT" > /dev/null 2>&1
        result=$?
        if [ $result -eq 0 ]; then
            end_ts=$(date +%s)
            echo "$WAITFORIT_HOST:$WAITFORIT_PORT is available after $((end_ts - start_ts)) seconds"
            break
        fi
        sleep 1
    done
    return $result
}

wait_for

# Your original script starts here
echo "Running wait_for_db script..." && python manage.py wait_for_db && echo "wait_for_db executed"
# echo "making migrations..." && python manage.py makemigrations
echo "trying to migrate..." && python manage.py migrate
echo "collecting static files..." && python manage.py collectstatic --no-input
echo "activating uwsgi..." && uwsgi --socket :8000 --master --enable-threads --module agilos.wsgi

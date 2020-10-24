#!/bin/sh

set -e

restart_error_handler() {
    (
        echo "Restart ${0} in 3 sec..."
        sleep 1
        echo "Restart ${0} in 2 sec..."
        sleep 1
        echo "Restart ${0} in 1 sec..."
        sleep 1
    )
    exec ${0}
}
trap restart_error_handler 0

echo "_______________________________________________________________________"
echo "$(date +%c) - ${0}"

(
    set -x

    poetry install --extras "postgres"

    ./manage.sh collectstatic --noinput --link
	./manage.sh makemigrations
	./manage.sh migrate

    ./manage.sh runserver 0.0.0.0:8000
    echo "runserver terminated with exit code: $?"
    sleep 3
    exit 1
)

exit 2

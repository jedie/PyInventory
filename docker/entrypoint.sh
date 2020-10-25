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

    ./manage.sh collectstatic --noinput
	./manage.sh makemigrations
	./manage.sh migrate

    exec poetry run uwsgi \
        --http inventory:8000 \
        --chdir /PyInventory \
        --wsgi-file /PyInventory/inventory_project/wsgi.py \
        --static-map /static=/PyInventory/static \
        --master \
        --processes 2 \
        --threads 2 \
        --ignore-sigpipe \
        --ignore-write-errors \
        --disable-write-exception \
        --http-auto-chunked \
        --http-keepalive
    echo "uwsgi terminated with exit code: $?"
    sleep 3
    exit 1
)

exit 2

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

if [ -d "/dist/" ] ; then
    (
        set -x
        pip3 install -U /dist/*.whl
    )
else
    (
        set -x
        pip3 install -U "pyinventory>=0.5.0rc1"
    )
fi
(
    set -x

    ./manage.py collectstatic --noinput
	./manage.py migrate

    uwsgi \
        --http inventory:8000 \
        --chdir /inventory/ \
        --wsgi-file /inventory/wsgi.py \
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

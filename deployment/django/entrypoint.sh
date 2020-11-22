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
        pip3 install -U "${PYTHON_PACKAGE_NAME}"
    )
fi

GUNICORN_CMD_ARGS=<<'EOF'
    --config /django/gunicorn.conf.py
    --bind "$(hostname):8000"
EOF

(
    set -x

    ./manage.py collectstatic --noinput
	./manage.py migrate

    su django -c "/usr/local/bin/gunicorn wsgi"

    echo "gunicorn terminated with exit code: $?"
    sleep 3
    exit 1
)

exit 2

#!/bin/bash

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-inventory_project.settings.local}

exec poetry run python3 manage.py "$@"

"""
    Django settings for local development with docker-compose usage
"""
import os as __os

from inventory_project.settings.local import *  # noqa


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': __os.environ['DB_NAME'],
        'USER': __os.environ['DB_USER'],
        'PASSWORD': __os.environ['DB_PASS'],
        'HOST': __os.environ['DB_HOST'],
        'PORT': __os.environ['DB_PORT'],
        'DEBUG_NAME': 'default',
        'CONN_MAX_AGE': 600,
    },
}

"""
    Django settings for docker usage (local and production)
"""
import os as __os

from inventory_project.settings.base import *  # noqa


HOSTNAME = __os.environ['HOSTNAME']

if HOSTNAME != 'localhost':
    print(f'Production mode on domain: {HOSTNAME!r}')
    DEBUG = False
    INTERNAL_IPS = ()
else:
    print('Local development mode')
    DEBUG = True
    INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', 'localhost')


ALLOWED_HOSTS = (HOSTNAME,)


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

"""
    Django settings for production usage
"""
import os as __os
from pathlib import Path as __Path

from inventory_project.settings.base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

INTERNAL_IPS = ()

ALLOWED_HOSTS = ('domain.tld',)  # TODO

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = __Path('secret.txt').resolve().open('r').read().strip()

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

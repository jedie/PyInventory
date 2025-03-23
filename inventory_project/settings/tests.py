# flake8: noqa: E405
"""
    Settings used to run tests
"""
import os

from inventory_project.settings.prod import *  # noqa


ALLOWED_HOSTS = ['testserver']


# _____________________________________________________________________________
# Manage Django Project

INSTALLED_APPS.append('manage_django_project')

# _____________________________________________________________________________


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'No individual secret for tests ;)'

DEBUG = True

# Speedup tests by change the Password hasher:
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

# _____________________________________________________________________________


# All tests should use django-override-storage!
# Set root to not existing path, so that wrong tests will fail:
STATIC_ROOT = '/not/exists/static/'
MEDIA_ROOT = '/not/exists/media/'


# _____________________________________________________________________________
# Playwright
# Avoid django.core.exceptions.SynchronousOnlyOperation. Playwright uses an event loop,
# even when using he sync API. Django only checks whether _any_ event loop is running,
# but not if _itself_ is running in an even loop.
# see https://github.com/microsoft/playwright-python/issues/439#issuecomment-763339612.
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', '1')

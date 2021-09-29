# flake8: noqa: E405, F403

from inventory_project.settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'No individual secret for tests ;)'

DEBUG = True

LOGGING['formatters']['colored']['format'] = (
    '%(log_color)s%(name)s %(levelname)8s %(cut_path)s:%(lineno)-3s %(message)s'
)

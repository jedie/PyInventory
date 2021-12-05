# flake8: noqa: E405, F403

from inventory_project.settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'No individual secret... But this settings should only be used in tests ;)'

# Run the tests as on production: Without DBEUG:
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ('127.0.0.1', '0.0.0.0', 'localhost')

LOGGING['formatters']['colored']['format'] = (
    '%(log_color)s%(name)s %(levelname)8s %(cut_path)s:%(lineno)-3s %(message)s'
)

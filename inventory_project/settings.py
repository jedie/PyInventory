"""
    Django settings
"""

import logging
import os as __os
from pathlib import Path as __Path

from django.utils.translation import ugettext_lazy as _


print('Use settings:', __file__)


# Build paths inside the project:
BASE_PATH = __Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'TODO: Read secret.txt ;)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Required for the debug toolbar to be displayed:
INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', 'localhost')

ALLOWED_HOSTS = INTERNAL_IPS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bx_py_utils',  # https://github.com/boxine/bx_py_utils
    'import_export',  # https://github.com/django-import-export/django-import-export
    'dbbackup',  # https://github.com/django-dbbackup/django-dbbackup
    'ckeditor',  # https://github.com/django-ckeditor/django-ckeditor
    'reversion',  # https://github.com/etianen/django-reversion
    'reversion_compare',  # https://github.com/jedie/django-reversion-compare
    'tagulous',  # https://github.com/radiac/django-tagulous
    'adminsortable2',  # https://github.com/jrief/django-admin-sortable2

    'inventory.apps.InventoryConfig',
]

ROOT_URLCONF = 'inventory_project.urls'
WSGI_APPLICATION = 'inventory_project.wsgi.application'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'inventory.middlewares.RequestDictMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [str(__Path(BASE_PATH, 'inventory_project', 'templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'inventory.context_processors.inventory_version_string',
            ],
        },
    },
]

if DEBUG:
    # Disable caches:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


if 'DB_HOST' in __os.environ:
    # docker-compose usage with postgres database
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
else:
    # local run with SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(__Path(BASE_PATH.parent, 'PyInventory-database.sqlite3')),
            # 'NAME': ':memory:'
            # https://docs.djangoproject.com/en/dev/ref/databases/#database-is-locked-errors
            'timeout': 30,
        }
    }
print(f'Use Database: {DATABASES["default"]["NAME"]!r}')

# _____________________________________________________________________________
# Internationalization

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]
LOCALE_PATHS = [
    __Path(BASE_PATH, 'locale')
]
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'Europe/Paris'
USE_TZ = True

# _____________________________________________________________________________
# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = str(__Path(BASE_PATH, 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = str(__Path(BASE_PATH, 'media'))

# _____________________________________________________________________________
# Django-dbbackup

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': str(__Path(BASE_PATH, 'backups'))}

# _____________________________________________________________________________
# Django-Debug-Toolbar

ENABLE_DJDT = __os.environ.get('ENABLE_DJDT') in ('true', '1')
if ENABLE_DJDT:
    print('Enable Django-Debug-Toolbar')
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

    DEBUG_TOOLBAR_PATCH_SETTINGS = True
    from debug_toolbar.settings import CONFIG_DEFAULTS as DEBUG_TOOLBAR_CONFIG  # noqa

    # Disable some more panels that will slow down the page:
    DEBUG_TOOLBAR_CONFIG['DISABLE_PANELS'].add('debug_toolbar.panels.sql.SQLPanel')
    DEBUG_TOOLBAR_CONFIG['DISABLE_PANELS'].add('debug_toolbar.panels.cache.CachePanel')

    # don't load jquery from ajax.googleapis.com, just use django's version:
    DEBUG_TOOLBAR_CONFIG['JQUERY_URL'] = STATIC_URL + 'admin/js/vendor/jquery/jquery.min.js'

    DEBUG_TOOLBAR_CONFIG['SHOW_TEMPLATE_CONTEXT'] = True
    DEBUG_TOOLBAR_CONFIG['SHOW_COLLAPSED'] = True  # Show toolbar collapsed by default.
    DEBUG_TOOLBAR_CONFIG['SHOW_TOOLBAR_CALLBACK'] = 'inventory_project.middlewares.djdt_show'

# _____________________________________________________________________________
# django-ckeditor

CKEDITOR_BASEPATH = STATIC_URL + 'ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'
CKEDITOR_CONFIGS = {
    'ItemModel.description': {
        'skin': 'moono-lisa',
        'removeButtons': 'Language',

        # plugins are here: site-packages/ckeditor/static/ckeditor/ckeditor/plugins
        'removePlugins': 'wsc,div,flash,iframe,bidi',
        'toolbar': 'full',
        'height': '25em',
        'width': '100%',
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
    },
    'LocationModel.description': {
        'skin': 'moono-lisa',
        'removeButtons': 'Language',

        # plugins are here: site-packages/ckeditor/static/ckeditor/ckeditor/plugins
        'removePlugins': 'wsc,div,flash,iframe,bidi',
        'toolbar': 'full',
        'height': '25em',
        'width': '100%',
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
    }
}

# _____________________________________________________________________________
# http://radiac.net/projects/django-tagulous/documentation/installation/#settings

TAGULOUS_NAME_MAX_LENGTH = 255
TAGULOUS_SLUG_MAX_LENGTH = 50
TAGULOUS_LABEL_MAX_LENGTH = TAGULOUS_NAME_MAX_LENGTH
TAGULOUS_SLUG_TRUNCATE_UNIQUE = 5
TAGULOUS_SLUG_ALLOW_UNICODE = False

# _____________________________________________________________________________
# cut 'pathname' in log output

old_factory = logging.getLogRecordFactory()


def cut_path(pathname, max_length):
    if len(pathname) <= max_length:
        return pathname
    return f'...{pathname[-(max_length - 3):]}'


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.cut_path = cut_path(record.pathname, 30)
    return record


logging.setLogRecordFactory(record_factory)

# -----------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'colored': {  # https://github.com/borntyping/python-colorlog
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s %(levelname)8s %(cut_path)s:%(lineno)-3s %(message)s',
        }
    },
    'handlers': {'console': {'class': 'colorlog.StreamHandler', 'formatter': 'colored'}},
    'loggers': {
        '': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'inventory': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
    },
}

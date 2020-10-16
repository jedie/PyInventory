"""
    Django settings
"""

import logging
from pathlib import Path as __Path

from debug_toolbar.settings import CONFIG_DEFAULTS as DEBUG_TOOLBAR_CONFIG
from django.utils.translation import ugettext_lazy as _


print('Use settings:', __file__)


# Build paths inside the project:
BASE_PATH = __Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'TODO: Read secret.txt ;)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1

# Required for the debug toolbar to be displayed:
INTERNAL_IPS = '*'

ALLOWED_HOSTS = INTERNAL_IPS


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'debug_toolbar',  # https://github.com/jazzband/django-debug-toolbar/
    'import_export',  # https://github.com/django-import-export/django-import-export
    'ckeditor',  # https://github.com/django-ckeditor/django-ckeditor
    'reversion',  # https://github.com/etianen/django-reversion
    'reversion_compare',  # https://github.com/jedie/django-reversion-compare

    'inventory.apps.InventoryConfig',
)

ROOT_URLCONF = 'inventory_project.urls'
WSGI_APPLICATION = 'inventory_project.wsgi.application'

MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_tools.middlewares.ThreadLocal.ThreadLocalMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(__Path(BASE_PATH, 'templates/'))],
        'OPTIONS': {
            'loaders': [
                (
                    'django.template.loaders.cached.Loader',
                    ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader'),
                )
            ],
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'django.template.context_processors.static',
            ],
        },
    }
]

if DEBUG:
    # Disable caches:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
    # Disable CacheLoader:
    TEMPLATES[0]['OPTIONS']['loaders'] = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

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
# Django-Debug-Toolbar

# Disable some more panels that will slow down the page:
DEBUG_TOOLBAR_CONFIG['DISABLE_PANELS'].add('debug_toolbar.panels.sql.SQLPanel')
DEBUG_TOOLBAR_CONFIG['DISABLE_PANELS'].add('debug_toolbar.panels.cache.CachePanel')

# don't load jquery from ajax.googleapis.com, just use django's version:
DEBUG_TOOLBAR_CONFIG['JQUERY_URL'] = STATIC_URL + 'admin/js/vendor/jquery/jquery.min.js'

DEBUG_TOOLBAR_CONFIG['SHOW_COLLAPSED'] = True  # Show toolbar collapsed by default.

# _____________________________________________________________________________
# django-ckeditor

CKEDITOR_BASEPATH = STATIC_URL + 'ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'
CKEDITOR_CONFIGS = {
    # 'ItemModel.description': {
    #     'toolbar': 'full',
    #     'height': '25em',
    #     'width': '100%',
    #     'removeButtons': 'Language,Flash,iframes,bidiltr'
    # },
    'ItemModel.description': {
        'skin': 'moono-lisa',
        # 'toolbar_Basic': [['Source', '-', 'Bold', 'Italic']],
        # 'toolbar_Full': [
        #     [
        #         'Styles',
        #         'Format',
        #         'Bold',
        #         'Italic',
        #         'Underline',
        #         'Strike',
        #         'SpellChecker',
        #         'Undo',
        #         'Redo',
        #     ],
        #     ['Link', 'Unlink', 'Anchor'],
        #     ['Image', 'Flash', 'Table', 'HorizontalRule'],
        #     ['TextColor', 'BGColor'],
        #     ['Smiley', 'SpecialChar'],
        #     ['Source'],
        # ],
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

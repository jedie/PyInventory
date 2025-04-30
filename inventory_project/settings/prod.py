"""
    Base Django settings
"""

import logging
from pathlib import Path as __Path


from django.utils.translation import gettext_lazy as _


###############################################################################

# Build paths relative to the project root:
BASE_PATH = __Path(__file__).parent.parent.parent
print(f'BASE_PATH:{BASE_PATH}')
assert __Path(BASE_PATH, 'inventory_project').is_dir()

###############################################################################
# PyInventory:

# Max length of Item/Location "path name" in change list:
TREE_PATH_STR_MAX_LENGTH = 70

###############################################################################


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Serve static/media files by Django?
# In production the Webserver should serve this!
SERVE_FILES = False


# SECURITY WARNING: keep the secret key used in production secret!
__SECRET_FILE = __Path(BASE_PATH, 'secret.txt').resolve()
if not __SECRET_FILE.is_file():
    print(f'Generate {__SECRET_FILE}')
    from secrets import token_urlsafe as __token_urlsafe

    __SECRET_FILE.write_text(__token_urlsafe(128))

SECRET_KEY = __SECRET_FILE.read_text().strip()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bx_django_utils',  # https://github.com/boxine/bx_django_utils
    'import_export',  # https://github.com/django-import-export/django-import-export
    'dbbackup',  # https://github.com/django-dbbackup/django-dbbackup
    'tinymce',  # https://github.com/jazzband/django-tinymce/
    'reversion',  # https://github.com/etianen/django-reversion
    'reversion_compare',  # https://github.com/jedie/django-reversion-compare
    'tagulous',  # https://github.com/radiac/django-tagulous
    'adminsortable2',  # https://github.com/jrief/django-admin-sortable2
    # https://github.com/jedie/django-tools/tree/master/django_tools/serve_media_app
    'django_tools.serve_media_app.apps.UserMediaFilesConfig',
    # https://github.com/jedie/django-tools/tree/master/django_tools/model_version_protect
    'django_tools.model_version_protect.apps.ModelVersionProtectConfig',
    #
    'inventory.apps.AppConfig',
]

ROOT_URLCONF = 'inventory_project.urls'
WSGI_APPLICATION = 'inventory_project.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

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

__TEMPLATE_DIR = __Path(BASE_PATH, 'inventory_project', 'templates')
assert __TEMPLATE_DIR.is_dir(), f'Directory not exists: {__TEMPLATE_DIR}'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [str(__TEMPLATE_DIR)],
        'APP_DIRS': True,
        'OPTIONS': {
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
                'inventory.context_processors.inventory_version_string',
            ],
        },
    },
]

# _____________________________________________________________________________

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# _____________________________________________________________________________

# Mark CSRF cookie as "secure" -> browsers sent cookie only with an HTTPS connection:
CSRF_COOKIE_SECURE = True

# Mark session cookie as "secure" -> browsers sent cookie only with an HTTPS connection:
SESSION_COOKIE_SECURE = True

# HTTP header/value combination that signifies a request is secure
# Your nginx.conf must set "X-Forwarded-Protocol" proxy header!
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# SecurityMiddleware should redirects all non-HTTPS requests to HTTPS:
SECURE_SSL_REDIRECT = True

# SecurityMiddleware should preload directive to the HTTP Strict Transport Security header:
SECURE_HSTS_PRELOAD = True

# Instruct modern browsers to refuse to connect to your domain name via an insecure connection:
SECURE_HSTS_SECONDS = 3600

# SecurityMiddleware should add the "includeSubDomains" directive to the Strict-Transport-Security
# header: All subdomains of your domain should be served exclusively via SSL!
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# _____________________________________________________________________________
# Internationalization

LANGUAGE_CODE = 'en'

LANGUAGES = [('ca', _('Catalan')), ('de', _('German')), ('en', _('English')), ('es', _('Spanish'))]
USE_I18N = True
TIME_ZONE = 'Europe/Paris'
USE_TZ = True

# _____________________________________________________________________________
# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = str(__Path(BASE_PATH, 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = str(__Path(BASE_PATH, 'media'))

# _____________________________________________________________________________
# Cache Backend

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# _____________________________________________________________________________
# Django-dbbackup

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': str(__Path(BASE_PATH, 'backups'))}

# _____________________________________________________________________________
# django-tinymce

TINYMCE_DEFAULT_CONFIG = {
    # https://www.tiny.cloud/docs/tinymce/latest/editor-size-options/
    'height': 500,
    'width': '90%',
    'resize': 'both',
    #
    # https://www.tiny.cloud/docs/tinymce/latest/menus-configuration-options/
    'menubar': 'edit view insert format tools table help',
    'browser_spellcheck': True,
    #
    # https://www.tiny.cloud/docs/tinymce/latest/plugins/
    'plugins': (
        'advlist,autolink,lists,link,image,charmap,preview,anchor,'
        'searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,'
        'help,wordcount'
    ),
    #
    # https://www.tiny.cloud/docs/tinymce/latest/available-toolbar-buttons/
    'toolbar': (
        'undo redo | blocks | '
        'bold italic backcolor | alignleft aligncenter '
        'alignright alignjustify | bullist numlist outdent indent | '
        'removeformat'
    ),
}


# _____________________________________________________________________________
# http://radiac.net/projects/django-tagulous/documentation/installation/#settings

TAGULOUS_NAME_MAX_LENGTH = 255
TAGULOUS_SLUG_MAX_LENGTH = 50
TAGULOUS_LABEL_MAX_LENGTH = TAGULOUS_NAME_MAX_LENGTH
TAGULOUS_SLUG_TRUNCATE_UNIQUE = 5
TAGULOUS_SLUG_ALLOW_UNICODE = False

SERIALIZATION_MODULES = {
    'xml': 'tagulous.serializers.xml_serializer',
    'json': 'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml': 'tagulous.serializers.pyyaml',
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
        'django_tools': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'inventory': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
    },
}

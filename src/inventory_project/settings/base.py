'''
    Base Django settings
'''

import logging
from pathlib import Path as __Path

from django.utils.translation import ugettext_lazy as _


###############################################################################

# Build paths relative to the project root:
PROJECT_PATH = __Path(__file__).parent.parent.parent
print(f'PROJECT_PATH:{PROJECT_PATH}')

if __Path('/.dockerenv').is_file():
    # We are inside a docker container
    BASE_PATH = __Path('/django_volumes')
    assert BASE_PATH.is_dir()
else:
    # Build paths relative to the current working directory:
    BASE_PATH = __Path().cwd().resolve()

print(f'BASE_PATH:{BASE_PATH}')

# Paths with Django dev. server:
# BASE_PATH...: .../django-for-runners
# PROJECT_PATH: .../django-for-runners/src
#
# Paths in Docker container:
# BASE_PATH...: /for_runners_volumes
# PROJECT_PATH: /usr/local/lib/python3.9/site-packages

###############################################################################


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Serve static/media files by Django?
# In production Caddy should serve this!
SERVE_FILES = False


# SECURITY WARNING: keep the secret key used in production secret!
__SECRET_FILE = __Path(BASE_PATH, 'secret.txt').resolve()
if not __SECRET_FILE.is_file():
    print(f'Generate {__SECRET_FILE}')
    from secrets import token_urlsafe as __token_urlsafe
    __SECRET_FILE.open('w').write(__token_urlsafe(128))

SECRET_KEY = __SECRET_FILE.open('r').read().strip()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'bx_django_utils',  # https://github.com/boxine/bx_django_utils
    'import_export',  # https://github.com/django-import-export/django-import-export
    'dbbackup',  # https://github.com/django-dbbackup/django-dbbackup
    'ckeditor',  # https://github.com/django-ckeditor/django-ckeditor
    'ckeditor_uploader',  # https://github.com/django-ckeditor/django-ckeditor
    'reversion',  # https://github.com/etianen/django-reversion
    'reversion_compare',  # https://github.com/jedie/django-reversion-compare
    'tagulous',  # https://github.com/radiac/django-tagulous
    'adminsortable2',  # https://github.com/jrief/django-admin-sortable2
    'axes',  # https://github.com/jazzband/django-axes
    'django_processinfo',  # https://github.com/jedie/django-processinfo/

    # https://github.com/jedie/django-tools/tree/master/django_tools/serve_media_app
    'django_tools.serve_media_app.apps.UserMediaFilesConfig',

    'inventory.apps.InventoryConfig',
]

ROOT_URLCONF = 'inventory_project.urls'
WSGI_APPLICATION = 'inventory_project.wsgi.application'
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django_processinfo.middlewares.ProcessInfoMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'inventory.middlewares.RequestDictMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'axes.middleware.AxesMiddleware',  # AxesMiddleware should be the last middleware
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(__Path(PROJECT_PATH, 'inventory_project', 'templates'))],
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
# django-processinfo

from django_processinfo import app_settings as PROCESSINFO  # noqa


PROCESSINFO.ADD_INFO = False  # Don't add info in HTML page

# _____________________________________________________________________________
# Django-dbbackup

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': str(__Path(BASE_PATH, 'backups'))}

# _____________________________________________________________________________
# django-ckeditor

CKEDITOR_BASEPATH = STATIC_URL + 'ckeditor/ckeditor/'
CKEDITOR_FILENAME_GENERATOR = 'inventory.ckeditor_upload.get_filename'
CKEDITOR_DEFAULT_CONFIG = {
    'skin': 'moono-lisa',
    'removeButtons': 'Language,Cut,Copy,Paste,Undo,Redo,Anchor',

    # plugins are here: .../site-packages/ckeditor/static/ckeditor/ckeditor/plugins
    # and here: https://github.com/ckeditor/ckeditor4/tree/major/plugins
    # See also: .../site-packages/ckeditor/static/ckeditor/ckeditor/build-config.js
    'removePlugins': (
        # Generated with .../dev-scripts/ckeditor_info.py
        'a11yhelp',
        'about',
        'adobeair',
        'ajax',
        'autoembed',
        # 'autogrow',
        'autolink',
        # 'basicstyles',
        'bbcode',
        'bidi',
        # 'blockquote',
        'clipboard',
        'codesnippet',
        'codesnippetgeshi',
        # 'colorbutton',
        # 'colordialog',
        'contextmenu',
        'copyformatting',
        'devtools',
        'dialog',
        'dialogadvtab',
        'div',
        'divarea',
        'docprops',
        # 'elementspath',
        'embed',
        'embedbase',
        'embedsemantic',
        'enterkey',
        # 'entities',
        # 'filebrowser',
        # 'filetools',
        'find',
        'flash',
        # 'floatingspace',
        # 'font',
        # 'format',
        'forms',
        # 'horizontalrule',
        'htmlwriter',
        'iframe',
        'iframedialog',
        # 'image',
        # 'image2',
        # 'indentblock',
        # 'indentlist',
        # 'justify',
        'language',
        # 'lineutils',
        # 'link',
        # 'list',
        # 'liststyle',
        'magicline',
        'mathjax',
        # 'maximize',
        # 'menubutton',
        'newpage',
        'notification',
        'notificationaggregator',
        'pagebreak',
        'pastefromgdocs',
        'pastefromword',
        'pastetext',
        'pastetools',
        'placeholder',
        'preview',
        'print',
        # 'removeformat',
        # 'resize',
        'save',
        'scayt',
        'selectall',
        'sharedspace',
        # 'showblocks',
        # 'showborders',
        'smiley',
        'sourcearea',
        'sourcedialog',
        'specialchar',
        'stylescombo',
        'stylesheetparser',
        'tab',
        # 'table',
        # 'tableresize',
        # 'tableselection',
        # 'tabletools',
        'templates',
        # 'toolbar',
        'uicolor',
        # 'undo',
        # 'uploadimage',
        # 'uploadwidget',
        'widget',
        'wsc',
        # 'wysiwygarea',
        'xml',
    ),
    'toolbar': 'full',
    'height': '25em',
    'width': '100%',
    'filebrowserWindowWidth': 940,
    'filebrowserWindowHeight': 725,
}
CKEDITOR_CONFIGS = {
    'ItemModel.description': CKEDITOR_DEFAULT_CONFIG,
    'LocationModel.description': CKEDITOR_DEFAULT_CONFIG
}
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_RESTRICT_BY_DATE = True
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_THUMBNAIL_SIZE = (300, 300)
CKEDITOR_IMAGE_QUALITY = 40
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_ALLOW_NONIMAGE_FILES = True

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
        'axes': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
        'django_tools': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'inventory': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
    },
}

# coding: utf-8

# Django settings for labman_ud project.

from unipath import Path
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
import djcelery
from celery.task.schedules import crontab

PROJECT_DIR = Path(__file__).ancestor(3)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-EN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL of the login page.
LOGIN_URL = '/login/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
# MEDIA_ROOT = ''
MEDIA_ROOT = PROJECT_DIR.child('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# STATIC_ROOT = ''
STATIC_ROOT = PROJECT_DIR.child('collected_static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR.child('static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$fshr_l3d%(b8yu21zi&amp;-khm5jo2(p%3ydx6@n1fm(0@=tyaap'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'labman_ud.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'labman_ud.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR.child('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'labman_ud.context_processors.global_vars',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # nested_inlines must be before django.contrib.admin
    # 'django_admin_bootstrapped',
    'suit',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',

    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

    # Re-usable applications
    'django_extensions',
    'logentry_admin',
    'ckeditor',
    'django_wysiwyg',

    # Custom applications with data models
    'entities.events',
    'entities.funding_programs',
    'entities.news',
    'entities.organizations',
    'entities.persons',
    'entities.projects',
    'entities.publications',
    'entities.utils',

    # Custom applications for data consulting only
    'charts',
    'semantic_search',

    # Zotero integration
    'generators.zotero_labman',

    # South: database migrations
    'south',

    'django_cleanup',

    # Celery: background task queueing system
    'djcelery',

    'pagination_bootstrap',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CKEDITOR_MEDIA_PREFIX = '/media/ckeditor_uploads/'
CKEDITOR_UPLOAD_PATH = PROJECT_DIR.child('media') + '/ckeditor_uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Full': [
            {'name': 'document', 'items': ['Source', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Copy', 'Paste', 'PasteText', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SpellChecker', 'Scayt']},
            '/',
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv']},
            {'name': 'justification', 'items': ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule', 'SpecialChar', 'PageBreak']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks', '-', 'About']}
        ]
    },
}

DJANGO_WYSIWYG_FLAVOR = 'ckeditor'

# Django Suit configuration example
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'labman_ud',
    # 'HEADER_DATE_FORMAT': 'l, j. F Y',
    # 'HEADER_TIME_FORMAT': 'H:i',

    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    # 'MENU_ICONS': {
    #    'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    # 'MENU': (
    #     'sites',
    #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #     {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    # ),

    # misc
    'LIST_PER_PAGE': 25
}

################################################
# project's global variables
################################################

# The default amount of items to show on a page if no number is specified.
PAGINATION_DEFAULT_PAGINATION = 10

# The number of items to the left and to the right of the current page to display (accounting for ellipses).
PAGINATION_DEFAULT_WINDOW = 3

# Determines whether an invalid page raises an Http404 or just sets the invalid_page context variable.
# True does the former and False does the latter.
PAGINATION_INVALID_PAGE_RAISES_404 = True

# Django email settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

PROJECTS_RECEPTOR_EMAILS = ['']
PROJECTS_SENDER_EMAIL = ''

BITLY_ACCESS_TOKEN = ''

TWEETPONY_CONSUMER_KEY = ''
TWEETPONY_CONSUMER_SECRET = ''
TWEETPONY_ACCESS_TOKEN = ''
TWEETPONY_ACCESS_TOKEN_SECRET = ''

ZOTERO_API_KEY = ''
ZOTERO_LIBRARY_ID = ''
ZOTERO_LIBRARY_TYPE = ''
ZOTERO_CRONTAB = crontab(hour='*/2')

# Celery config
djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler'

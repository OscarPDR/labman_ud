# -*- encoding: utf-8 -*-

from .base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

ADMINS = (
    ('', ''),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.sqlite3',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

USE_X_FORWARDED_HOST = True
FORCE_SCRIPT_NAME = '/labman'

STATIC_URL = '/labman/static/'

MEDIA_URL = '/labman/media/'
MEDIA_ROOT = ''

DEBUG_TOOLBAR_PATCH_SETTINGS = False

####################################################################################################
###     Email settings
####################################################################################################

# Django email settings
EMAIL_HOST = ''
EMAIL_PORT = 587

EMAIL_SENDER_ADDRESS = ''
GENERAL_NOTIFICATIONS_ADDRESSES = ['']


####################################################################################################
###     News twitter configuration: https://github.com/Mezgrman/TweetPony & http://karmacracy.com/
####################################################################################################

TWEETPONY_CONSUMER_KEY = ''
TWEETPONY_CONSUMER_SECRET = ''
TWEETPONY_ACCESS_TOKEN = ''
TWEETPONY_ACCESS_TOKEN_SECRET = ''

KARMACRACY_URL = ''

NEWS_DETAIL_BASE_URL = ''
NEWS_TITLE_MAX_LENGTH = 120


####################################################################################################
###     Zotero settings: https://www.zotero.org/
####################################################################################################

ZOTERO_API_KEY = ''
ZOTERO_LIBRARY_ID = ''
ZOTERO_LIBRARY_TYPE = ''

ZOTERO_CRONTAB = crontab(minute='*/15')
ZOTERO_LOG_PATH = ''

####################################################################################################
###     Celery settings: http://www.celeryproject.org/
####################################################################################################

djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


####################################################################################################
###     RDF & Virtuoso settings
####################################################################################################

HTTP_PROXY = ''
HTTPS_PROXY = ''

RDF_URI = ''

D2R_TO_VIRTUOSO = True
D2R_SPARQL_URL = ''
D2R_MAPPING_PATH = ''

VIRTUOSO_ODBC = ''
VIRTUOSO_GRAPH = RDF_URI

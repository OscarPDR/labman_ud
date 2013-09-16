"""
WSGI PROD config for labman_ud project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

# Activate virtualenv
activate_this = os.path.expanduser('/home/morelab/.virtualenvs/labman/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

sys.path.append('/home/morelab/.virtualenvs/labman/labman_ud/labman_ud')
sys.path.append('/home/morelab/.virtualenvs/labman/labman_ud/labman_ud/labman_ud')

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labman_ud.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "labman_ud.settings.prod"

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

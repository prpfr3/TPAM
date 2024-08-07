"""
WSGI config for TPAM project.

This module contains the WSGI application used by Django's development server and any production WSGI deployments. It should expose a module-level variable named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also might make sense to replace the whole Django WSGI application with a custom one that later delegates to the Django one. For example, you could introduce WSGI middleware here, or combine a Django application with an application of another framework.

For more information, visit
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TPAM.settings")

"""
This application object is used by any WSGI server configured to use this file. This includes Django's development server, if the WSGI_APPLICATION setting points here.
"""

# application = Cling(get_wsgi_application()) # Use for development
application = get_wsgi_application()  # Use for production

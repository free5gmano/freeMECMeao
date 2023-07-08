"""
WSGI config for kube5gMEAO project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kube5gMEAO.settings')

application = get_wsgi_application()

try:
    os.mkdir("NSD")
except Exception as e:
    pass

try:
    os.mkdir("VNFD")
except Exception as e:
    pass

try:
    os.mkdir("AppD")
except Exception as e:
    pass
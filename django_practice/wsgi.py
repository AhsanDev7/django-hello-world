"""
WSGI config for django_practice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_practice.settings')
static_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "staticfiles"))

app = get_wsgi_application()
app = WhiteNoise(app, root=static_root)
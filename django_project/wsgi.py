"""
WSGI config for sig_health_slackbot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from django_project.sentry import sentry_init

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings.live")

application = get_wsgi_application()
sentry_init()

import sentry_sdk
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration


def sentry_init():
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=settings.ENVIRONMENT,
        send_default_pii=True,
    )

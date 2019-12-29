from django.apps import AppConfig


class SigHealthConfig(AppConfig):
    name = "apps.sig_health"
    verbose_name = "시그 헬스"

    def ready(self):
        import apps.sig_health.receivers  # noqa

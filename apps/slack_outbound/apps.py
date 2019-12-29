from django.apps import AppConfig


class SlackOutboundConfig(AppConfig):
    name = "apps.slack_outbound"
    verbose_name = "슬랙 아웃바운드"

    def ready(self):
        import apps.slack_outbound.receivers  # noqa

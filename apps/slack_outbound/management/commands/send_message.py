from apps.slack_outbound.models import MessageTask
from django.core.management.base import BaseCommand

from django_project.sentry import sentry_init


class Command(BaseCommand):
    help = "sig-헬스 봇으로 채널에 메시지를 보냅니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--text",
            nargs="?",
            type=str,
            required=True,
            help="보낼 텍스트입니다.",
            dest="text",
        )

    def handle(self, *args, **options):
        sentry_init()
        MessageTask.objects.create(text=options["text"])

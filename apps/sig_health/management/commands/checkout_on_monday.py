from django.core.management.base import BaseCommand

from django_project.sentry import sentry_init


class Command(BaseCommand):
    help = "매주 초에 실행될, 정회원 탈락이 이루어지는 커맨드입니다."

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        sentry_init()

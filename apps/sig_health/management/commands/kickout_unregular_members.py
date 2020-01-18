from apps.sig_health.models import Member
from django.core.management.base import BaseCommand

from django_project.sentry import sentry_init


class Command(BaseCommand):
    help = "선택한 주의 운동 횟수가 채워지지 않았을 경우, 정회원에서 탈락됩니다. 기본: 지난 주"

    def add_arguments(self, parser):
        parser.add_argument(
            "-w",
            "--weekdelta",
            nargs="+",
            type=int,
            default=-1,
            help="몇 주 전 데이터를 검사할지 고릅니다.",
            dest="weekdelta",
        )

    def handle(self, *args, **options):
        sentry_init()
        for member in Member.regular_members.all():
            if not member.has_passed_minimum_on_week(weekdelta=options["weekdelta"]):
                member.is_regular = False
                member.save()

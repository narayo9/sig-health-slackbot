import traceback

import sentry_sdk
from apps.slack_outbound.models import EmojiTask, MessageTask, ReplyTask
from django.core.management import BaseCommand

from django_project.utils import sentry_init


class Command(BaseCommand):
    def handle(self, *args, **options):
        sentry_init()
        task_list = [
            *MessageTask.unexecuted.all(),
            *ReplyTask.unexecuted.all(),
            *EmojiTask.unexecuted.all(),
        ]
        print(f"총 {len(task_list)} 개 준비 완료")

        executed = 0
        for task in [
            *MessageTask.unexecuted.all(),
            *ReplyTask.unexecuted.all(),
            *EmojiTask.unexecuted.all(),
        ]:
            try:
                task.execute()
            except BaseException:
                traceback.print_exc()
                sentry_sdk.capture_exception()
            else:
                executed += 1

        print(f"총 {executed} 개 작업 완료")

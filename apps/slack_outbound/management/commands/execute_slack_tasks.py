from apps.slack_outbound.models import EmojiTask, MessageTask, ReplyTask
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for task in [
            *MessageTask.unexecuted.all(),
            *ReplyTask.unexecuted.all(),
            *EmojiTask.unexecuted.all(),
        ]:
            task.execute()

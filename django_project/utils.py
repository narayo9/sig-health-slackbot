import slack
from django.conf import settings
from django.db import models
from django.utils import timezone
from django_enumfield import enum
from django_enumfield.db.fields import EnumField
from model_utils.models import TimeStampedModel


class TaskStatus(enum.Enum):
    READY = 0
    PROGRESS = 1
    SUCCESS = 2
    FAIL = 3

    __default__ = READY


class UnexecutedTaskManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(execute_at__lte=timezone.now(), status=TaskStatus.READY)
        )


class Task(TimeStampedModel):
    status = EnumField(TaskStatus)
    execute_at = models.DateTimeField(null=False, blank=False, verbose_name="실행 일시")

    objects = models.Manager()
    unexecuted = UnexecutedTaskManager()

    class Meta:
        abstract = True


def use_slack():
    client = slack.WebClient(token=settings.BOTUSER_OAUTH_ACCESS_TOKEN)

    def chat_postMessage(text: str, thread_ts: str = None):  # noqa: N802
        return client.chat_postMessage(
            channel=settings.SIG_HEALTH_CHANNEL, thread_ts=thread_ts, text=text
        )

    def reactions_add(timestamp: str, name: str):
        return client.reactions_add(
            channel=settings.SIG_HEALTH_CHANNEL, name=name, timestamp=timestamp
        )

    return {
        "chat_postMessage": chat_postMessage,
        "reactions_add": reactions_add,
        "client": client,
    }

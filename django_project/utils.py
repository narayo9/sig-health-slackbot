import datetime

import slack
from dateutil.relativedelta import MO, SU, relativedelta
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
    execute_at = models.DateTimeField(
        null=False, blank=True, verbose_name="실행 일시", auto_now_add=True
    )

    objects = models.Manager()
    unexecuted = UnexecutedTaskManager()

    def is_ready(self):
        return self.execute_at <= timezone.now() and self.status == TaskStatus.READY

    class Meta:
        abstract = True


def use_slack():
    from apps.sig_health.models import Meta

    meta = Meta.objects.get_main()
    client = slack.WebClient(token=meta.oauth_access_token)

    def chat_postMessage(text: str, thread_ts: str = None):  # noqa: N802
        return client.chat_postMessage(
            channel=meta.channel_id, thread_ts=thread_ts, text=text
        )

    def reactions_add(timestamp: str, name: str):
        return client.reactions_add(
            channel=meta.channel_id, name=name, timestamp=timestamp
        )

    return {
        "chat_postMessage": chat_postMessage,
        "reactions_add": reactions_add,
        "client": client,
    }


def get_week_start_end(weekdelta: int = 0):
    return (
        (
            datetime.datetime.now()
            + relativedelta(weekday=MO(-1))
            + relativedelta(weeks=weekdelta)
        ).date(),
        (
            datetime.datetime.now()
            + relativedelta(weekday=SU(+1))
            + relativedelta(weeks=weekdelta)
        ).date(),
    )

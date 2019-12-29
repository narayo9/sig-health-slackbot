import traceback

from django.db import models
from sentry_sdk import capture_exception

from django_project.utils import Task, TaskStatus, use_slack


class MessageTask(Task):
    text = models.TextField(verbose_name="보낼 텍스트", null=False, blank=False)

    def execute(self, commit=True):
        chat_postMessage = use_slack().get("chat_postMessage")  # noqa: N806
        try:
            chat_postMessage(text=self.text)
        except BaseException:
            traceback.print_exc()
            capture_exception()
            self.status = TaskStatus.FAIL
        else:
            self.status = TaskStatus.SUCCESS
        finally:
            if commit:
                self.save()


class ReplyTask(Task):
    thread_ts = models.CharField(
        verbose_name="댓글을 달기 위한 쓰레드", null=False, blank=False, max_length=100
    )
    text = models.TextField(verbose_name="보낼 텍스트", null=False, blank=False)

    def execute(self, commit=True):
        chat_postMessage = use_slack().get("chat_postMessage")  # noqa: N806
        try:
            chat_postMessage(text=self.text, thread_ts=self.thread_ts)
        except BaseException:
            traceback.print_exc()
            capture_exception()
            self.status = TaskStatus.FAIL
        else:
            self.status = TaskStatus.SUCCESS
        finally:
            if commit:
                self.save()


class EmojiTask(Task):
    name = models.CharField(
        max_length=100, verbose_name="이모지 이름", null=False, blank=False
    )
    timestamp = models.CharField(
        max_length=100, verbose_name="이모지 달 메세지 타임스탬프", null=False, blank=False
    )

    def execute(self, commit=True):
        reactions_add = use_slack().get("reactions_add")
        try:
            reactions_add(name=self.name, timestamp=self.timestamp)
        except BaseException:
            traceback.print_exc()
            capture_exception()
            self.status = TaskStatus.FAIL
        else:
            self.status = TaskStatus.SUCCESS
        finally:
            if commit:
                self.save()

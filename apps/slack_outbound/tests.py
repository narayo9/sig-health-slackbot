from apps.slack_outbound.models import EmojiTask, MessageTask, ReplyTask
from django.conf import settings
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from django_project.utils import TaskStatus, use_slack


class OutboundSimpleTests(SimpleTestCase):
    def test_message(self):
        chat_postMessage = use_slack().get("chat_postMessage")  # noqa: N806
        chat_postMessage(text="yayaya")

    def test_reply(self):
        chat_postMessage = use_slack().get("chat_postMessage")  # noqa: N806
        chat_postMessage(thread_ts="1577569017.007000", text="와! 댓글!")

    def test_emoji(self):
        reactions_add = use_slack().get("reactions_add")
        reactions_add(name="thumbsup", timestamp="1577569017.007000")


class OutboundTests(TestCase):
    def test_message(self):
        task = MessageTask.objects.create(execute_at=timezone.now(), text="텍스트1")
        task.execute()
        self.assertEqual(task.status, TaskStatus.SUCCESS)

    def test_reply(self):
        client = use_slack().get("client")
        response = client.chat_postMessage(
            channel=settings.SIG_HEALTH_CHANNEL, text="댓글 테스트"
        )
        thread_ts = response.data["ts"]
        task = ReplyTask.objects.create(
            execute_at=timezone.now(), text="댓글이드아", thread_ts=thread_ts
        )
        task.execute()
        self.assertEqual(task.status, TaskStatus.SUCCESS)

    def test_emoji(self):
        client = use_slack().get("client")
        response = client.chat_postMessage(
            channel=settings.SIG_HEALTH_CHANNEL, text="이모지 테스트"
        )
        thread_ts = response.data["ts"]
        task = EmojiTask.objects.create(
            execute_at=timezone.now(), name="thumbsup", timestamp=thread_ts
        )
        task.execute()
        self.assertEqual(task.status, TaskStatus.SUCCESS)

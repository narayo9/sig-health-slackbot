import slack
from django.conf import settings
from django.test import SimpleTestCase


class OutboundTests(SimpleTestCase):
    def setUp(self):
        self.client = slack.WebClient(token=settings.BOTUSER_OAUTH_ACCESS_TOKEN)

    def test_message(self):
        self.client.chat_postMessage(channel="CRR629M3L", text="웹훅은 기능이 너무 약하네요...")

    def test_reply(self):
        self.client.chat_postMessage(
            channel="CRR629M3L", thread_ts="1577569017.007000", text="와! 댓글!"
        )

    def test_emoji(self):
        self.client.reactions_add(
            channel="CRR629M3L", name="thumbsup", timestamp="1577569017.007000"
        )

from apps.slack_outbound.models import EmojiTask, MessageTask, ReplyTask
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=MessageTask)
def send_message_when_created(instance: MessageTask, created, **kwargs):
    if created:
        if instance.is_ready():
            instance.execute()


@receiver(post_save, sender=EmojiTask)
def send_emoji_when_created(instance: EmojiTask, created, **kwargs):
    if created:
        if instance.is_ready():
            instance.execute()


@receiver(post_save, sender=ReplyTask)
def reply_when_created(instance: ReplyTask, created, **kwargs):
    if created:
        if instance.is_ready():
            instance.execute()

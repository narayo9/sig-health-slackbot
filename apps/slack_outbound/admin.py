from apps.slack_outbound.models import EmojiTask, MessageTask, ReplyTask
from django.contrib import admin

admin.site.register(MessageTask)
admin.site.register(EmojiTask)
admin.site.register(ReplyTask)

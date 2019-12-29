import traceback
from parser.events import MessageChannels, ReactionAdded
from parser.events.base import SlackEvent

from apps.sig_health.models import Member, Meta, WorkoutAdmit
from apps.slack_outbound.models import EmojiTask
from sentry_sdk import capture_exception


def create_tasks(event: SlackEvent):
    meta = Meta.objects.get_main()
    if (
        isinstance(event, ReactionAdded)
        and event.reaction == meta.admit_emoji
        and event.item_user
    ):
        admitted_by, _ = Member.objects.get_or_create(slack_id=event.user)
        member, _ = Member.objects.get_or_create(slack_id=event.item_user)
        admit = WorkoutAdmit(
            admitted_by=admitted_by, member=member, thread_ts=event.item.ts
        )
        try:
            admit.full_clean()
        except BaseException:
            traceback.print_exc()
            capture_exception()
        else:
            admit.save()

    if (
        isinstance(event, MessageChannels)
        and Member.regular_members.filter(slack_id=event.user).exists()
    ):
        EmojiTask.objects.create(name=meta.regular_member_emoji, timestamp=event.ts)

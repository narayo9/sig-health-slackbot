import traceback
from parser.events import MessageChannels, ReactionAdded

from apps.sig_health.models import Member, Meta, WorkoutAdmit
from apps.slack_outbound.models import EmojiTask
from sentry_sdk import capture_exception


def handle_admit_emoji_added(event: ReactionAdded):
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


def handle_regular_member_message(event: MessageChannels):
    meta = Meta.objects.get_main()
    EmojiTask.objects.create(name=meta.regular_member_emoji, timestamp=event.ts)

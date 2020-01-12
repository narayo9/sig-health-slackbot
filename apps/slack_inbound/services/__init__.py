from parser import parse
from parser.events import MessageChannels, ReactionAdded

from apps.sig_health.models import Member, Meta
from apps.slack_inbound.services.handlers import (
    handle_admit_emoji_added,
    handle_regular_member_message,
)


def process_slack_event(request_body: str):
    _, event = parse(request_body)
    meta = Meta.objects.get_main()

    if (
        isinstance(event, ReactionAdded)
        and event.reaction == meta.admit_emoji
        and event.item_user
    ):
        handle_admit_emoji_added(event)

    if (
        isinstance(event, MessageChannels)
        and Member.regular_members.filter(slack_id=event.user).exists()
    ):
        handle_regular_member_message(event)

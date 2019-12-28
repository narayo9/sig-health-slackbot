from parser.events.base import (
    SlackEvent,
    SlackEventField,
    SlackEventObjectField,
    SlackEventTimestampField,
)


class URLVerification(SlackEvent):
    type = SlackEventField()
    token = SlackEventField()
    challenge = SlackEventField()

    def get_response_data(self):
        return {"challenge": self.challenge}

    @classmethod
    def is_raw_of_event(cls, raw_dict: dict):
        return raw_dict.get("type") == "url_verification"


class ReactionAddedItem(SlackEvent):
    type = SlackEventField()
    channel = SlackEventField()
    ts = SlackEventTimestampField()


class ReactionAdded(SlackEvent):
    type = SlackEventField()
    user = SlackEventField()
    reaction = SlackEventField()
    item_user = SlackEventField()
    item = SlackEventObjectField(object_cls=ReactionAddedItem)
    event_ts = SlackEventTimestampField()

    @classmethod
    def is_raw_of_event(cls, raw_dict: dict):
        return raw_dict.get("type") == "reaction_added"


class MessageChannelsEvent(SlackEvent):
    type = SlackEventField()
    channel = SlackEventField()
    user = SlackEventField()
    text = SlackEventField()
    ts = SlackEventTimestampField()
    event_ts = SlackEventTimestampField()
    channel_type = SlackEventField()


class MessageChannels(SlackEvent):
    token = SlackEventField()
    team_id = SlackEventField()
    api_app_id = SlackEventField()
    event = SlackEventObjectField(object_cls=MessageChannelsEvent)
    type = SlackEventField()
    event_id = SlackEventField()
    event_time = SlackEventTimestampField()

    @classmethod
    def is_raw_of_event(cls, raw_dict: dict):
        return (
            raw_dict.get("type") == "event_callback"
            and raw_dict.get("event")
            and raw_dict["event"].get("type") == "message"
        )

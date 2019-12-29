from parser.events.base import SlackEvent, SlackEventField, SlackEventObjectField


class URLVerification(SlackEvent):
    type = SlackEventField()
    token = SlackEventField()
    challenge = SlackEventField()

    def get_response_data(self):
        return {"challenge": self.challenge}

    @classmethod
    def is_raw_of_event(cls, raw_dict: dict):
        return raw_dict.get("type") == "url_verification"


class ReactionItem(SlackEvent):
    type = SlackEventField()
    channel = SlackEventField()
    ts = SlackEventField()


class ReactionAdded(SlackEvent):
    type = SlackEventField()
    user = SlackEventField()
    reaction = SlackEventField()
    item_user = SlackEventField()
    item = SlackEventObjectField(object_cls=ReactionItem)
    event_ts = SlackEventField()

    @classmethod
    def is_raw_of_event(cls, raw_dict: dict):
        return raw_dict.get("type") == "reaction_added"


class ReactionRemoved(SlackEvent):
    type = SlackEventField()
    user = SlackEventField()
    reaction = SlackEventField()
    item_user = SlackEventField()
    item = SlackEventObjectField(object_cls=ReactionItem)
    event_ts = SlackEventField()

    @classmethod
    def is_raw_of_event(cls, raw_dict: dict):
        return raw_dict.get("type") == "reaction_removed"


class MessageChannelsEvent(SlackEvent):
    type = SlackEventField()
    channel = SlackEventField()
    user = SlackEventField()
    text = SlackEventField()
    ts = SlackEventField()
    event_ts = SlackEventField()
    channel_type = SlackEventField()


class MessageChannels(SlackEvent):
    type = SlackEventField()
    channel = SlackEventField()
    user = SlackEventField()
    text = SlackEventField()
    ts = SlackEventField()
    event_ts = SlackEventField()
    channel_type = SlackEventField()

    @classmethod
    def is_raw_of_event(cls, raw_dict: dict):
        return raw_dict.get("type") == "message"

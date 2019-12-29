import json
from parser.events import event_types
from parser.events.base import SlackEvent
from parser.exceptions import UnhandledEventType
from pprint import pprint
from typing import Tuple, Union


def parse(event_raw: bytes) -> Tuple[Union[dict], SlackEvent]:
    event_dict = json.loads(event_raw.decode("utf-8"))
    pprint(event_dict)
    return parse_dict(event_dict)


def parse_dict(event_raw_dict: dict) -> Tuple[Union[dict], SlackEvent]:
    event_dict = event_raw_dict.get("event", None) or event_raw_dict
    for event_type in event_types:
        if event_type.is_raw_of_event(event_dict):
            event = event_type(**event_dict)
            return event.get_response_data(), event
    raise UnhandledEventType

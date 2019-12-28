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
    for event in event_types:
        if event.is_raw_of_event(event_raw_dict):
            event = event(**event_raw_dict)
            return event.get_response_data(), event
    raise UnhandledEventType

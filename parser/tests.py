from parser.events import MessageChannels, ReactionAdded, URLVerification
from parser.exceptions import UnhandledEventType
from parser.parse import parse_dict

from django.test import SimpleTestCase


class ParserTests(SimpleTestCase):
    def test_url_verification(self):
        challenge = "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"
        response_data, event = parse_dict(
            {
                "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",
                "challenge": challenge,
                "type": "url_verification",
            }
        )
        self.assertEqual(response_data["challenge"], challenge)
        self.assertIsInstance(event, URLVerification)

    def test_reaction_added(self):
        response_data, event = parse_dict(
            {
                "type": "reaction_added",
                "user": "U024BE7LH",
                "reaction": "thumbsup",
                "item_user": "U0G9QF9C6",
                "item": {
                    "type": "message",
                    "channel": "C0G9QF9GZ",
                    "ts": "1360782400.498405",
                },
                "event_ts": "1360782804.083113",
            }
        )
        self.assertEqual(response_data, {})
        self.assertIsInstance(event, ReactionAdded)

    def test_message_channel(self):
        response_data, event = parse_dict(
            {
                "api_app_id": "AS43WE2DT",
                "authed_users": ["US448AG7P"],
                "event": {
                    "blocks": [
                        {
                            "block_id": "yn3",
                            "elements": [
                                {
                                    "elements": [{"name": "hooray", "type": "emoji"}],
                                    "type": "rich_text_section",
                                }
                            ],
                            "type": "rich_text",
                        }
                    ],
                    "channel": "CRR629M3L",
                    "channel_type": "channel",
                    "client_msg_id": "6dc36338-8ace-464e-b5bb-f7e69f7f617f",
                    "event_ts": "1577562298.003300",
                    "team": "T03FE7QJV",
                    "text": ":hooray:",
                    "ts": "1577562298.003300",
                    "type": "message",
                    "user": "UCL25JV2R",
                },
                "event_id": "EvS61CH48P",
                "event_time": 1577562298,
                "team_id": "T03FE7QJV",
                "token": "B1IDpHbsMUa7NgtJTgT33ena",
                "type": "event_callback",
            }
        )

        self.assertIsInstance(event, MessageChannels)

    def test_raise_unhandled_event_type(self):
        with self.assertRaises(UnhandledEventType):
            parse_dict({"type": "some strange type"})

import logging

from .fields import SlackEventField, SlackEventObjectField, SlackEventTimestampField

__all__ = [
    "SlackEvent",
    "SlackEventField",
    "SlackEventTimestampField",
    "SlackEventObjectField",
]

logger = logging.getLogger(__name__)


class SlackEventMetadata:
    def __init__(self, parents=None):
        self.fields = {}

        if parents:
            for parent in parents:
                self.fields.update(parent.fields)


class SlackEventMetaclass(type):
    def __new__(cls, name, bases, attrs):
        new_cls = super(SlackEventMetaclass, cls).__new__(cls, name, bases, attrs)

        new_cls._meta = SlackEventMetadata(
            parents=[
                base._meta
                for base in bases
                if isinstance(getattr(base, "_meta", None), SlackEventMetadata)
            ]
        )

        for attr_name, attr in attrs.items():
            if isinstance(attr, SlackEventField):
                cls.init_field(attr_name, attr, new_cls)
            elif attr_name in new_cls._meta.fields:
                new_cls._meta.fields.pop(attr_name)

        return new_cls

    @staticmethod
    def init_field(attr_name, field: SlackEventField, new_cls):
        if attr_name == "api_data":
            logger.warning(
                "%s.%s: ConfigurationWarning: "
                "Field name `api_data` is reserved. This can lead to unexpected behavior.",  # noqa: B950
                new_cls.__module__,
                new_cls.__name__,
            )

        if field.api_name is None:
            field.api_name = attr_name

        # get_FIELD_display method 설정하기
        if field.choices:

            def get_FIELD_display(self):  # noqa: N802
                return field.choices.get(
                    getattr(self, attr_name), getattr(self, attr_name)
                )

            function_name = f"get_{attr_name}_display"
            get_FIELD_display.__name__ = function_name
            setattr(new_cls, function_name, get_FIELD_display)

        new_cls._meta.fields[attr_name] = field


class SlackEvent(metaclass=SlackEventMetaclass):
    def __init__(self, **kwargs):
        for (
            attr_name,
            field,
        ) in self._meta.fields.items():  # type: (str, SlackEventField)
            value = field.parse(kwargs.get(attr_name))
            setattr(self, attr_name, value)

    @classmethod
    def is_raw_of_event(cls, raw_dict: dict) -> bool:
        return False

    def get_response_data(self):
        return {}

from datetime import datetime


class SlackEventField:
    NOT_SET = object()

    def __init__(self, api_name=None, required=False, choices=None, default=NOT_SET):
        self.api_name = api_name
        self.required = required
        self.default = default
        self.choices = choices

    @property
    def has_default(self):
        return self.default is not self.NOT_SET

    def get_raw_value(self, data, key=None):
        if key is None:
            key = self.api_name
        if self.has_default:
            return data.get(key, self.default)
        elif self.required:
            return data[key]
        else:
            return data.get(key, None)

    def parse(self, value):
        return value


class SlackEventTimestampField(SlackEventField):
    def __init__(self, is_millisecond=False, **kwargs):
        super().__init__(**kwargs)
        self.is_millisecond = is_millisecond

    def parse(self, value):
        value = super().parse(value)
        value = float(value)

        if self.is_millisecond:
            value /= 1000

        return datetime.fromtimestamp(value)


class SlackEventObjectField(SlackEventField):
    def __init__(self, object_cls, **kwargs):
        super().__init__(**kwargs)
        self.object_cls = object_cls

    def parse(self, value):
        value = super().parse(value)
        return self.object_cls(**value)

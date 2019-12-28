class SlackParserException(BaseException):
    default_msg = "슬랙 이벤트 파싱 중 에러 발생"

    def __init__(self, msg=default_msg):
        self.msg = msg

    def __str__(self):
        return f"{self.__class__.__name__}: {self.msg}"


class UnhandledEventType(SlackParserException):
    default_msg = "처리되지 않은 슬랙 에러 타입"


class TypeImproperlyConfigured(SlackParserException):
    default_msg = "설정된 타입이 아님"

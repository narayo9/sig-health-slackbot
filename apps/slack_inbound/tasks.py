from parser import parse

from apps.slack_inbound.services import create_tasks


def process_slack_event(request_body: str):  # TODO: celery로 변경
    _, event = parse(request_body)
    create_tasks(event)

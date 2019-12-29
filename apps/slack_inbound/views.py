from parser import parse

from django.db import transaction
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response

from .tasks import process_slack_event


class SlackInboundView(views.APIView):
    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        request_body = request.body.decode("utf-8")
        response_data, event = parse(request_body)
        process_slack_event(request_body)
        return Response(response_data)

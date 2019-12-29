from parser import parse

from apps.slack_inbound.services import create_tasks
from django.db import transaction
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response


class SlackInboundView(views.APIView):
    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        response_data, event = parse(request.body)
        create_tasks(event)
        return Response(response_data)

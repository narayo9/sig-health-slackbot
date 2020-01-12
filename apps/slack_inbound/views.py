import threading
from parser import parse

from apps.slack_inbound.services import process_slack_event
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response


class SlackInboundView(views.APIView):
    def post(self, request: Request, *args, **kwargs):
        request_body = request.body.decode("utf-8")
        response_data, event = parse(request_body)
        new_thread = threading.Thread(target=process_slack_event, args=[request_body])
        new_thread.start()
        return Response(response_data)

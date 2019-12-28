from parser import parse

from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response


class SlackEventView(views.APIView):
    def post(self, request: Request, *args, **kwargs):
        response_data, _ = parse(request.body)
        return Response(response_data)

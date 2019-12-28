from django.urls import path

from . import views

urlpatterns = [
    path("inbound/", views.SlackInboundView.as_view(), name="slack-inbound-api")
]

from django.urls import path

from . import views

urlpatterns = [path("events", views.SlackEventView.as_view(), name="slack-event-api")]

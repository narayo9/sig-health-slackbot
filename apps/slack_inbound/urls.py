from django.urls import path

from . import views

urlpatterns = [path("", views.SlackEventView.as_view(), name="slack-event-api")]

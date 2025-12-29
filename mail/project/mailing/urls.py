from django.urls import path

from . import views

urlpatterns = [
    path("send_feedback/", views.feedback_view, name="send_feedback"),
]

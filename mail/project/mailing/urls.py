from django.urls import path

from . import views

urlpatterns = [
    path("send_feedback/", views.feedback_view, name="send_feedback"),
    path(
        "send_feedback_with_attachments/",
        views.feedback_extend_view,
        name="send_feedback_attachments",
    ),
]

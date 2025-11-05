from django.urls import path

from . import views

urlpatterns = [
    path("register_user/", views.create_user, name="register_user"),
]

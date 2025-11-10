from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="forms_example/index.html"),
        name="index_page",
    ),
    path("register_user/", views.create_user, name="register_user"),
    path("auth_user/", views.auth_user, name="auth_user"),
    path("logout/", LogoutView.as_view(next_page="index_page"), name="logout"),
]

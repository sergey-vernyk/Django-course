from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="django_signals/login.html"),
        name="login",
    ),
    path(
        "",
        views.get_users_projects,
        name="user-projects",
    ),
    path(
        "add/<int:project_id>/",
        views.add_user_to_project,
        name="add-user-to-project",
    ),
    path(
        "remove/<int:project_id>/",
        views.remove_user_from_project,
        name="remove-user-from-project",
    ),
    path(
        "clear/",
        views.clear_user_projects,
        name="clear-user-projects",
    ),
]

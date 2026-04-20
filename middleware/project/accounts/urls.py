# accounts/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("danger/", views.dangerous_view, name="clickjaking"),
    path("beta/dashboard/", views.beta_dashboard_view, name="beta_dashboard"),
]

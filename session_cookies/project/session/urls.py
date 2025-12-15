from django.urls import path

from . import views

urlpatterns = [
    # cookies
    path("set-cookies/", views.set_cookies, name="set_cookies"),
    path("delete-cookies/", views.delete_cookies, name="delete_cookies"),
    path("get-cookies/", views.get_cookies, name="get_cookies"),
    # session
    path("set-session/", views.set_session, name="set_session"),
    path("get-session/", views.get_session, name="get_session"),
]

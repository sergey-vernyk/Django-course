from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("create/", views.create_post, name="post_create"),
    path("edit/<int:post_id>/", views.edit_post, name="post_edit"),
    path("publish/<int:post_id>/", views.publish_post, name="post_publish"),
]

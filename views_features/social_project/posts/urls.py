from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/<int:pk>/edit/", views.post_update, name="post_update"),
    path("posts/<int:pk>/remove/", views.post_remove, name="post_remove"),
    path(
        "posts/<int:post_id>/add/<int:category_id>/",
        views.post_add_category,
        name="post_add_category",
    ),
    path(
        "posts/<int:post_id>/remove/<int:category_id>/",
        views.post_remove_category,
        name="post_remove_category",
    ),
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/remove/", views.category_remove, name="category_remove"),
    path(
        "categories/get-or-create/",
        views.category_get_or_create,
        name="category_get_or_create",
    ),
    path(
        "categories/update-or-create/",
        views.category_update_or_create,
        name="category_update_or_create",
    ),
    path("debug", views.debug_api, name="debug_api"),
]

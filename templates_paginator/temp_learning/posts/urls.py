from django.urls import path

from .views import category_list, post_detail, post_list

urlpatterns = [
    path("", post_list, name="post_list"),
    path("post/<int:post_id>/", post_detail, name="post_detail"),
    path("categories/", category_list, name="category_list"),
]

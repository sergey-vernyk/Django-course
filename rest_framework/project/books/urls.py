from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookListCreateAPIView.as_view(), name="book_list_create"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="products"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/", views.remove_from_cart, name="remove_from_cart"),
]

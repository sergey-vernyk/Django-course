from django.urls import path

from . import views

urlpatterns = [
    # /products
    # path("", views.product_list, name="product_list"),
    path("", views.ProductListView.as_view(), name="product_list"),
    # path(
    #     # /products/5/samsung/
    #     "<int:product_pk>/<slug:product_slug>/",
    #     views.product_detail,
    #     # name бажано завжди писати, щоб потім його використовували
    #     # в функції 'reverse'
    #     name="product_detail",
    # ),
    path(
        "<int:product_pk>/<slug:product_slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
]

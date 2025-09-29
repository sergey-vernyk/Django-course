from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from .models import Product


def product_list(request: HttpRequest) -> HttpResponse:
    """Функція обробника вхідного запиту на отримання списку товарів."""
    products = Product.objects.all()
    return render(request, "products/product_list.html", context={"products": products})


def product_detail(
    request: HttpRequest, product_pk: int, product_slug: str
) -> HttpResponse:
    """Функція обробника вхідного запиту на отримання одного товару з pk та slug."""
    product = Product.objects.filter(pk=product_pk, slug=product_slug).get()
    return render(
        request,
        template_name="products/product_detail.html",
        context={"product": product},
    )

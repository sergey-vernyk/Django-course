from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request: HttpRequest) -> HttpResponse:
    """Список товарів."""
    products = Product.objects.all()
    cart: list = request.session.get("cart", [])
    return render(
        request,
        template_name="shop/product_list.html",
        context={
            "products": products,
            "cart_count": len(cart),
        },
    )


def add_to_cart(request: HttpRequest) -> JsonResponse:
    """Додавання товару в кошик в сесію."""
    product_id = request.POST.get("product_id")
    cart: list = request.session.get("cart", [])

    if product_id not in cart:
        cart.append(product_id)
        request.session["cart"] = cart

    return JsonResponse({"status": "ok", "cart_count": len(cart)})


def remove_from_cart(request: HttpRequest) -> JsonResponse:
    """Видалення товару з кошика з сесії."""
    product_id = request.POST.get("product_id")
    cart: list = request.session.get("cart", [])

    if product_id in cart:
        cart.remove(product_id)
        request.session["cart"] = cart

    return JsonResponse({"status": "ok", "cart_count": len(cart)})

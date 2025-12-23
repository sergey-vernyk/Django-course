import time

from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page


def slow_view(_: HttpRequest) -> HttpResponse:
    result = cache.get("slow_result")

    if result is None:
        time.sleep(3)
        cache.set("slow_result", "Done!")
        return HttpResponse("Закешовано")

    return HttpResponse("Дістали з кешу!")


def users_view(request: HttpRequest) -> HttpResponse:
    users = cache.get("users")
    print(f"Отримано з кешу: {users}")

    if users is None:
        print("Кеш пустий!")
        users = list(User.objects.all())
        cache.set("users", users)

    return render(request, "caching/users.html", {"users": users})


def create_user(_: HttpRequest) -> HttpResponse:
    user = User.objects.create(
        username=f"user_{int(time.time())}",
    )
    cache.delete("users")
    return HttpResponse(f"User {user.username} created!")


@cache_page(60)
def homepage(request: HttpRequest) -> HttpResponse:
    return render(request, "caching/home.html")

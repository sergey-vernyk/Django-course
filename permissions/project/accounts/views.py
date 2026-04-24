from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

User = get_user_model()


def custom_403(request: HttpRequest, exception: Exception) -> HttpResponse:
    """
    Кастомна сторінка для переадресації,
    коли користувач немає доступу до ресурсу.
    """
    return render(
        request,
        "403.html",
        {"title": "Access denied", "message": str(exception) or "Access denied"},
        status=403,
    )


def register_view(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    """Реєстрація користувача в системі."""
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"],
        )
        return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    """Автентифікація зареєстрованого користувача."""
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("post_list")

        return render(request, "accounts/login.html", {"error": "Invalid credentials."})

    return render(request, "accounts/login.html")


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """Вихід з системи - завершення сесії користувача."""
    logout(request)
    return redirect("login")

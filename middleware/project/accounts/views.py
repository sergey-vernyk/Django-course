from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


def register_view(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    """Реєстрація користувача в системі."""
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"],
            role=request.POST["role"],
        )
        messages.success(request, "User has been registered successfully!")
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
            messages.success(request, "Login success!")
            return redirect("profile")

        messages.error(request, "Username or password is invalid!")
        return render(request, "accounts/login.html", {"error": "Invalid credentials."})

    return render(request, "accounts/login.html")


@login_required(login_url=reverse_lazy("login"))
def profile_view(request: HttpRequest) -> HttpResponse:
    """Оновлення профілю автентифікованого користувача."""
    if request.method == "POST":
        request.user.first_name = request.POST["name"]
        request.user.save()
        messages.success(request, "User first name has been updated!")

    return render(request, "accounts/profile.html", {"user": request.user})


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """Вихід з системи - завершення сесії користувача."""
    logout(request)
    return redirect("login")


@csrf_exempt
def dangerous_view(request: HttpRequest) -> HttpResponse:
    """Симуляція вразливості `clickjaking`."""
    if request.method == "POST":
        return HttpResponse("<h1>💀 You just got hacked!</h1>")

    return HttpResponse("""
        <form method="post">
            <button type="submit" style="
                width:100%;
                height:100vh;
                font-size:30px;
            ">
                Delete account
            </button>
        </form>
    """)


def beta_dashboard_view(request: HttpRequest) -> HttpResponse:
    """Покращений дашбоард в бета версії (симуляція відповіді)."""

    username = getattr(request.user, "username", "anon")
    # raise Exception("Oops!")
    return HttpResponse(f"""
        <h1>🚀 Beta Dashboard</h1>

        <p>Welcome, <b>{username}</b></p>
        <p>Request ID: {getattr(request, "request_id", "-")}</p>
        <p>Beta bucket: {getattr(request, "beta_bucket", "-")}</p>

        <hr>

        <h3>Experimental features:</h3>
        <ul>
            <li>⚡ New analytics engine</li>
            <li>🧪 A/B testing panel</li>
            <li>📊 Real-time metrics</li>
        </ul>
    """)

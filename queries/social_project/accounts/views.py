from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import AuthForm


def auth_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect("/posts")

            form.add_error(None, "Invalid username or password")

            return render(
                request,
                template_name="accounts/user_auth.html",
                context={"form": form},
            )
    else:
        form = AuthForm()

    return render(
        request,
        template_name="accounts/user_auth.html",
        context={"form": form},
    )

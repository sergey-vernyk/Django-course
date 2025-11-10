from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import AuthForm, UserCreatingForm


def handle_basic_form(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = request.POST.dict()
        print(data)
        data.pop("csrfmiddlewaretoken")
        return render(request, "forms/basic.html", context={"data": data})

    return render(request, "forms/basic.html")


def handle_textarea_form(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")

        return render(request, "forms/textarea.html", context={"data": data})

    return render(request, "forms/textarea.html")


def handle_inputs_form(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")

        file = request.FILES.get("file")
        if file is not None:
            with open(f"{settings.MEDIA_ROOT}/{file.name}", "wb") as f:
                f.write(file.read())

            data["file"] = f"{settings.MEDIA_URL}{file.name}"
        return render(request, "forms/inputs.html", context={"data": data})

    return render(request, "forms/inputs.html")


def handle_checkbox_radio_form(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")

        return render(request, "forms/checkbox_radio.html", context={"data": data})

    return render(request, "forms/checkbox_radio.html")


def handle_select_form(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")

        return render(request, "forms/selects.html", context={"data": data})

    return render(request, "forms/selects.html")


def create_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserCreatingForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(
                request,
                template_name="forms_example/user_register.html",
                context={"form": form, "success": True},
            )
    else:
        form = UserCreatingForm()

    return render(request, "forms_example/user_register.html", context={"form": form})


def auth_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect("/forms")

            form.add_error(None, "Invalid username or password")

            return render(
                request,
                template_name="forms_example/user_authorization.html",
                context={"form": form},
            )
    else:
        form = AuthForm()

    return render(
        request,
        template_name="forms_example/user_authorization.html",
        context={"form": form},
    )

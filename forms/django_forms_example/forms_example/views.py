from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


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

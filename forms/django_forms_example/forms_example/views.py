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

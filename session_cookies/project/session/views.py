from django.http import HttpRequest, HttpResponse


def set_cookies(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookies set!")
    response.set_cookie("test_key", str(request.user))
    return response


def get_cookies(request: HttpRequest) -> HttpResponse:
    cookies = request.COOKIES.get("test_key")
    return HttpResponse(cookies)


def delete_cookies(_: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookies deleted!")
    response.delete_cookie("test_key")
    return response


def set_session(request: HttpRequest) -> HttpResponse:
    request.session["color"] = "red"
    return HttpResponse("Color saved!")


def get_session(request: HttpRequest) -> HttpResponse:
    color = request.session.get("color", "unknown")
    return HttpResponse(f"Color is {color}")

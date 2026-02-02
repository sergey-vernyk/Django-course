from contextvars import ContextVar
from uuid import uuid4

from django.http import HttpRequest, HttpResponse

request_id_var = ContextVar("request_id", default="<no-id>")


class RequestIdMiddleware:
    """
    Додає унікальний ідентифікатор запиту в змінну контексту
    для передачі її в лог.
    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = str(uuid4())
        request_id_var.set(request_id)

        response = self.get_response(request)
        return response

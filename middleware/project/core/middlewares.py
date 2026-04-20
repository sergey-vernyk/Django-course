from collections.abc import Callable
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse

# Загальна схема 'обгортання' view middleware
#
# Request ->
#    Middleware A (request)
#    Middleware B (request)
#        -> VIEW ->
#    Middleware B (response)
#    Middleware A (response)
# <- Response

# Middleware - це глобальний рівень

# Якщо логіка потрібна:
# - тільки для одного view -> decorator
# - для всіх запитів -> middleware


class SimpleMiddleware:
    # викликається тільки один раз(!) при старті сервера
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        # 'get_response' параметр обов'язковий(!) і метод приймає тільки цей один параметр
        # метод може бути використаний для конфігурації та ініціалізації
        # глобального стану middleware
        self.get_response = get_response

    # 'обгортка' навколо усього циклу запиту -> відповіді
    def __call__(self, request: HttpRequest) -> HttpResponse:
        # код, який буде виконано для кожного(!) запиту перед викликом view
        # (і пізніше проміжного програмного забезпечення).
        response = self.get_response(request)
        # код, який буде виконано для кожного запиту/відповіді
        # після виклику view
        return response

    # останній контроль перед тим як код view виконається
    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable[..., HttpResponse],
        view_args: Any,
        view_kwargs: Any,
    ) -> HttpResponse | None:
        # повертає або HttpResponse або None

        # викликається після middleware, але до виклику view,
        # може заблокувати view, коли поверне HttpResponse,
        # дивитись, який саме view викликається та його параметри,
        # змінити логіку доступу до view

        # Якщо поверне None, то Django продовжить виконання запиту,
        # шляхом виклику інших process_view() з інших middleware
        # та виконання цього view
        ...

    # це страховка на випадок падіння view
    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> HttpResponse | None:
        # повинен повернути HttpResponse або None

        # викликається якщо view впав з Exception (будь-яким, наслідуваним від Exception класу)
        # якщо повертає None, то спрацює обробка помилок Django
        # за замовченням, але якщо повернеться HttpResponse,
        # то Django поверне цей же response до браузера (може бути також JsonResponse)

        # НЕ викликається, якщо exception оброблений іншим middleware вище
        ...

    # middleware, який працює з HTML вже після виконання view
    def process_template_response(
        self, request: HttpRequest, response: TemplateResponse
    ) -> TemplateResponse:
        # викликається одразу після того як view завершила виконання
        # і якщо response має метод render() (до речі, TemplateResponse об'єкт відповіді має його)
        # використовується для модифікації контексту (context_data), підміни шаблону (template_name),
        # або для створення взагалі нового об'єкту TemplateResponse для відповіді,
        # та додавання глобальних даних
        ...

    # викликається для КОЖНОГО response (навіть якщо була помилка)
    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse: ...

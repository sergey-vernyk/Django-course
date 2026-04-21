import logging
import random
import uuid
from collections.abc import Callable
from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

# Загальна схема 'обгортання' view middleware
#
# Request ->
#    Middleware A (request)
#    Middleware B (request)
#        -> VIEW ->
#    Middleware B (response)
#    Middleware A (response)
# <- Response

# Новий стиль написання Middleware (Ти сам керуєш порядком виконання)

# __call__()
#    ├── перед-обробка запиту
#    ├── виклик view
#    ├── пост-обробка відповіді

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


class BetaAccessMiddlewareOld(MiddlewareMixin):
    """
    Middleware для контролю доступу до beta-функціоналу
    в старому варіанті написання різними hooks.

    Виконує:
    - перевірку доступу через whitelist ролей та rollout-групи
    - поступове включення фічі (A/B rollout)
    - додавання до request атрибутів (request_id, beta_bucket)
    - аудит доступу та відмов у доступі
    """

    role_whitelist = {"admin", "teacher"}
    blocked_agents = {"curl", "wget", "python-requests", "httpx"}

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        super().__init__(get_response)
        self.rollout_percentage = 20

    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable[..., HttpResponse],
        view_args: Any,
        view_kwargs: Any,
    ) -> None | HttpResponse:
        print("[OLD] ENTER view processing")
        beta_bucket = random.randint(1, 100)
        request.beta_bucket = beta_bucket

        if "/beta/" not in request.path:
            return None

        if not request.user.is_authenticated:
            logger.warning("[BETA] login required to use beta features.")
            return HttpResponseForbidden("Login required for beta")

        user = request.user

        is_whitelisted_user = user.role in self.role_whitelist
        is_in_rollout_group = beta_bucket <= self.rollout_percentage

        # view і не запуститься, якщо ця умова буде True
        if not (is_whitelisted_user or is_in_rollout_group):
            return HttpResponseForbidden("<h2>Not in beta group!</h2>")

        print("[OLD] EXIT view processing")
        return None

    def process_request(self, request: HttpRequest) -> None | HttpResponse:
        print("[OLD] ENTER request processing")
        request.request_id = str(uuid.uuid4())
        user_agent = request.headers.get("User-Agent", "")

        if any(agent in user_agent.lower() for agent in self.blocked_agents):
            logger.warning(
                "[BETA] user-agent '%s' was attempted to access to beta features.",
                user_agent,
            )
            return HttpResponseForbidden("Bot traffic blocked")

        print("[OLD] EXIT request processing")
        return None

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        print("[OLD] ENTER response processing")
        if "/beta/" in request.path:
            if response.status_code == 200:
                logger.info(
                    "[BETA] user '%s' bucket %s got access to beta features.",
                    getattr(request.user, "username", "anon"),
                    getattr(request, "beta_bucket", "-"),
                )
            elif response.status_code == 403:
                logger.warning(
                    "[BETA] user '%s' was attempted to use beta features.",
                    getattr(request.user, "username", "anon"),
                )

        response["X-Trace-Id"] = getattr(request, "request_id", "-")
        print("[OLD] EXIT response processing")
        return response

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> HttpResponse:
        print("[OLD] ENTER exception processing")
        logger.error(
            "[BETA] request_id '%s': %s",
            getattr(request, "request_id", "-"),
            str(exception),
        )

        print("[OLD] EXIT exception processing")
        return HttpResponseForbidden("<h2>Something went wrong</h2>")


class BetaAccessMiddlewareNew:
    """
    Middleware для контролю доступу до beta-функціоналу
    в новому варіанті з використанням __call__() методу.

    Виконує:
    - перевірку доступу через whitelist ролей та rollout-групи
    - поступове включення фічі (A/B rollout)
    - додавання до request атрибутів (request_id, beta_bucket)
    - аудит доступу та відмов у доступі
    """

    role_whitelist = {"admin", "teacher"}
    blocked_agents = {"curl", "wget", "python-requests"}

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
        self.rollout_percentage = 20

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # обробка запиту (process_request() в старій версії)
        print("[NEW] ENTER request processing")
        request.request_id = str(uuid.uuid4())

        user_agent = request.headers.get("User-Agent", "")

        # view і не запуститься, якщо ця умова буде True
        if any(agent in user_agent.lower() for agent in self.blocked_agents):
            logger.warning(
                "[BETA] user-agent '%s' was attempted to access to beta features.",
                user_agent,
            )
            return HttpResponseForbidden("Bot traffic blocked")

        # логіка обробки перед view (process_view() в старій версії)
        beta_bucket = random.randint(1, 100)
        request.beta_bucket = beta_bucket

        if "/beta/" in request.path:
            if not request.user.is_authenticated:
                logger.warning("[BETA] login required to use beta features.")
                return HttpResponseForbidden("Login required for beta")

            # доступ є якщо користувач або в whitelist, або в rollout
            is_whitelisted_user = request.user.role in self.role_whitelist
            is_in_rollout_group = beta_bucket <= self.rollout_percentage

            if not (is_whitelisted_user or is_in_rollout_group):
                return HttpResponseForbidden("<h2>Not in beta group!</h2>")

        print("[NEW] EXIT request processing")

        # виконання view
        print("[NEW] ENTER view processing")
        response = self.get_response(request)
        print("[NEW] EXIT view processing")

        # --- спрацює код нижче навіть якщо була відловлена помилка ---

        # обробка відповіді від view (process_response() в старій версії)
        print("[NEW] ENTER response processing")
        if "/beta/" in request.path:
            if response.status_code == 200:
                logger.info(
                    "[BETA] user '%s' bucket %s got access to beta features.",
                    getattr(request.user, "username", "anon"),
                    getattr(request, "beta_bucket", "-"),
                )
            elif response.status_code == 403:
                logger.warning(
                    "[BETA] user '%s' was attempted to use beta features.",
                    getattr(request.user, "username", "anon"),
                )

        response["X-Trace-Id"] = getattr(request, "request_id", "-")
        print("[NEW] EXIT response processing")
        return response

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> HttpResponse:
        print("[NEW] ENTER process_exception()")
        logger.error(
            "[BETA] request_id '%s': %s",
            getattr(request, "request_id", "-"),
            str(exception),
        )

        print("[NEW] EXIT process_exception()")
        return HttpResponseForbidden("<h2>Something went wrong</h2>")

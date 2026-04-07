import uuid

from celery.result import AsyncResult
from django.contrib.auth import get_user_model, hashers, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from .models import Application, UserProfile
from .tasks.api import process_application
from .tasks.demo import calculate_sum, hash_passwords, long_task, unstable_task
from .tasks.emails import send_welcome_email

# pyright: reportFunctionMemberAccess=false
# pyright: reportCallIssue=false


def run_long_task(_: HttpRequest) -> JsonResponse:
    """Симуляція виконання довгої задачі."""
    task: AsyncResult = long_task.delay()

    return JsonResponse(
        {
            "message": "Long task started",
            "task_id": task.id,
        }
    )


def run_calculation(_: HttpRequest) -> JsonResponse:
    """Симуляція розрахунку задачі на навантаження процесора."""
    task: AsyncResult = calculate_sum.delay()

    return JsonResponse(
        {
            "message": "Calculation started",
            "task_id": task.id,
        }
    )


def run_unstable_task(_: HttpRequest) -> JsonResponse:
    """Симуляція задачі, яка може викинути випадково помилку."""
    task: AsyncResult = unstable_task.delay()

    return JsonResponse(
        {
            "message": "Unstable task started",
            "task_id": task.id,
        }
    )


def run_hashing_passwords_task(_: HttpRequest) -> JsonResponse:
    """Симуляція задачі, яка виконує хешування паролів, які навантажують процесор."""
    task: AsyncResult = hash_passwords.apply_async()

    return JsonResponse(
        {
            "message": "Task for hashing passwords started.",
            "task_id": task.id,
        }
    )


def get_task_result(_: HttpRequest, task_id: uuid.UUID) -> JsonResponse:
    """
    Отримання результату задачі по її ID,
    якщо `ignore_result=False` в `@shared_task` декораторі.
    """
    result = AsyncResult(str(task_id))

    return JsonResponse(
        {
            "status": result.status,
            "ready": result.ready(),
            "successful": result.successful(),
            "result": result.result if result.ready() else None,
        }
    )


def application_view(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    """
    Створення заявки в БД та її обробка асинхронно
    через Celery задачу.
    """
    if request.method == "POST":
        # створюємо заявку в базі
        app = Application.objects.create(user=request.user)
        # задача стартує через 10 секунд
        process_application.apply_async((app.pk,), countdown=10)
        return redirect("application")

    return render(request, "accounts/application.html")


def register_view(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    """
    Реєстрація користувача в БД та відправлення
    йому на пошту email асинхронно.
    """
    if request.method == "POST":
        user, created = get_user_model().objects.get_or_create(
            username=request.POST["username"],
            email=request.POST["email"],
            password=hashers.make_password(request.POST["password"]),
        )

        # створюємо користувача, якщо такого ще немає
        if created:
            UserProfile.objects.create(user=user)  # створюємо пов'язаний profile
            login(request, user)  # одразу авторизуємо користувача
            # email відправляється асинхронно через Celery
            send_welcome_email.delay(user.pk)
            return redirect("register")

        return HttpResponse("User already registered.")

    return render(request, "accounts/register.html")

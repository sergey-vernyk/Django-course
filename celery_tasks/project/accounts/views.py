import uuid

from celery.result import AsyncResult
from django.http import JsonResponse
from django.http.request import HttpRequest

from .tasks.demo import calculate_sum, hash_passwords, long_task, unstable_task

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

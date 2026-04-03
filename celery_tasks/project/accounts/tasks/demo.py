import random
import time

from celery import Task, shared_task
from django.contrib.auth.hashers import make_password


@shared_task(ignore_result=True)
def long_task() -> str:
    """
    Імітація довгої операції:
    - задача "засинає" на 10 секунд.
    - `ignore_result=True` означає, що результат не буде
        збережений у `result backend`.
    """
    time.sleep(10)

    return "Task finished after 10 seconds"


@shared_task
def calculate_sum() -> int:
    """
    CPU-bound задача:
    обчислення великої суми займає процесорний час.

    Добре показує, як Celery може винести
    важке обчислення з основного web-запиту.
    """
    return sum(range(10000000))


@shared_task(bind=True, max_retries=3)
def unstable_task(self: Task) -> str:
    """
    Імітуємо нестабільну поведінку:
    іноді задача падає випадково.

    `bind=True` дає доступ до самого обє'кту задачі,
    через який можна викликати повторний запуск `retry()`.

    `max_retries=3` означає: Celery спробує виконати задачу максимум 3 рази.

    """
    if random.choice([True, False]):
        # Якщо сталася помилка —
        # задача повториться через 5 секунд.
        raise self.retry(countdown=5)

    return "Task succeeded"


@shared_task
def hash_passwords() -> list[str]:
    """
    Генеруємо список паролів.

    `make_password` використовує хешування,
    що є CPU-bound операцією.

    Для демо беремо лише перші 10,
    щоб не перевантажувати систему.
    """
    passwords = [f"user{i}" for i in range(5000)]
    return [make_password(p) for p in passwords[:10]]

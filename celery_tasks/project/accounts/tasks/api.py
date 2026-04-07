import requests
from celery import Task, shared_task
from django.db import DatabaseError, transaction

from ..models import Application


@shared_task(
    bind=True,  # дає доступ до поточної задачі (self), навіть якщо retry виконується через autoretry_for
    # автоматичний retry тільки для очікуваних помилок
    autoretry_for=(
        requests.Timeout,
        requests.ConnectionError,
        DatabaseError,
    ),
    retry_backoff=True,  # затримка між retry буде поступово збільшуватись
    retry_jitter=True,  # додає випадковий розкид часу між retry
    retry_kwargs={"max_retries": 5},  # максимум 5 повторних спроб
    acks_late=True,  # задача підтвердиться тільки після повного завершення
)
def process_application(self: Task, application_id: int) -> None:
    """
    Імітація доступу на сторонній API з затримкою
    для "перевірки" і оновлення статусу application
    для користувача.
    """
    with transaction.atomic():  # зміни в БД виконуються атомарно
        app = Application.objects.get(id=application_id)

        if app.status == "done":  # захист від повторної обробки
            return

        response = requests.post(
            "https://httpbin.org/delay/3",
            json={"email": app.user.email},
            timeout=5,  # timeout обов'язковий для зовнішніх API
        )

        response.raise_for_status()  # HTTP помилки не ігноруються

        app.external_id = response.json().get("url")
        app.status = "done"
        # оновлюємо тільки потрібні поля
        app.save(update_fields=["status", "external_id"])

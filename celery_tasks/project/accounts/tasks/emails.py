import logging
from smtplib import SMTPException

from celery import Task, shared_task
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import DatabaseError, transaction

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,  # дає доступ до поточної задачі і дозволяє використовувати self.retry()
    retry_backoff=True,  # затримка між retry буде зростати автоматично
    retry_jitter=True,  # додає випадковий розкид часу, щоб уникати одночасних повторів
    retry_kwargs={"max_retries": 3},  # максимум 3 повторні спроби
    acks_late=True,  # задача підтвердиться тільки після успішного виконання
)
def send_welcome_email(self: Task, user_id: int) -> None:
    """
    Відправлення пошти для нового зареєстрованого користувача
    та проставлення статусу відправлення.
    """
    with transaction.atomic():  # усі зміни в БД виконуються як одна транзакція
        try:
            user = get_user_model().objects.select_related("profile").get(id=user_id)

            if user.profile.email_sent:  # захист від повторної відправки email
                return

            send_mail(
                subject="Welcome!",
                message=f"Hello {user.username}, thanks for registration.",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,  # помилки email не приховуються
            )

            user.profile.email_sent = True
            user.profile.save()

        except ObjectDoesNotExist:
            logger.error("User with id %d not found.", user_id)
            # retry тут не потрібен, бо користувача реально не існує
        except SMTPException as e:
            logger.error("Error with SMTP server: %s.", str(e))
            raise self.retry(exc=e)  # тимчасова помилка SMTP — retry має сенс

        except DatabaseError as e:
            logger.error("Error with PostgreSQL server: %s.", str(e))
            raise self.retry(exc=e)  # тимчасова проблема БД — retry можливий

        except Exception as e:
            logger.error("Unexpected error: %s.", str(e))
            raise  # невідома помилка — краще не retry автоматично

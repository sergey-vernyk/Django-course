import logging
from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

UserModel = get_user_model()
logger = logging.getLogger(__name__)


@shared_task
def remind_create_application(user_id: int) -> None:
    """Відправляє користувачу з `user_id` лист з нагадуванням."""
    user = UserModel.objects.filter(id=user_id).first()

    if user is None:
        return

    if user.applications.exists():
        return

    send_mail(
        subject="Don't forget your application",
        message="Please create your application. This is a one-time reminder.",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )

    logger.info("One-time reminder sent to %s", user.email)


@shared_task
def deactivate_inactive_users() -> None:
    """Деактивує користувачів в БД якщо, вони не входили в систему більше ніж 30 днів."""
    threshold = timezone.now() - timedelta(days=30)

    users = UserModel.objects.select_related("profile").filter(
        is_active=True,
        last_login__lt=threshold,
    )

    deactivated_count = 0

    for user in users:
        if user.applications.exists():
            continue

        user.is_active = False
        user.save(update_fields=["is_active"])
        deactivated_count += 1
        logging.info("Deactivated user %s", user.email)

    logging.info("Deactivated %d users", deactivated_count)

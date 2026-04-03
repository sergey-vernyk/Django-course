# імпорт Celery app при старті Django, щоб Celery задачі автоматично реєструвалися
from .celery import app as celery_app

# показує, що пакет офіційно віддає назовні тільки 'celery_app'
# навіть при 'from core import import *'
__all__ = ("celery_app",)

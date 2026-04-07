import os

from celery import Celery

# явно встановлюємо шлях до налаштувань Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("my_project")

# namespace='CELERY' означає всі налаштування для Celery
# повинні мати `CELERY_` префікс.
app.config_from_object("django.conf:settings", namespace="CELERY")

# авто-пошук задач в указаних модулях
app.autodiscover_tasks(packages=["accounts.tasks"])

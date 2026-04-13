import os

from celery import Celery
from celery.schedules import crontab

# явно встановлюємо шлях до налаштувань Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("my_project")

# namespace='CELERY' означає всі налаштування для Celery
# повинні мати `CELERY_` префікс.
app.config_from_object("django.conf:settings", namespace="CELERY")

# авто-пошук задач в указаних модулях
app.autodiscover_tasks(packages=["accounts.tasks", "accounts.tasks.periodic"])


app.conf.beat_schedule = {
    "deactivate_inactive_users": {
        "task": "accounts.tasks.periodic.deactivate_inactive_users",
        # UTC (для України треба відняти 3 години)
        "schedule": crontab(minute="*/2"),
    }
}

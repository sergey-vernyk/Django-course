from django.apps import AppConfig


class DjangoSignalsConfig(AppConfig):
    name = "django_signals"

    def ready(self) -> None:
        # обов'язково робимо імпорт тут,
        # а не вгорі модуля
        from . import signals

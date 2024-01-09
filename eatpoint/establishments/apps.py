# fmt: off
from django.apps import AppConfig


class EstablishmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "establishments"

    def ready(self):
        """Слушатель сигнала"""
        import establishments.signals
# fmt: on

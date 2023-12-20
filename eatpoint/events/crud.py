from django.db.models import QuerySet

from establishments.models import Establishment

from .models import Event, TypeEvent


def establishment_exists(est_id: int) -> bool:
    """Проверка существования Заведения в базе данных."""
    return Establishment.objects.filter(establishment_id=est_id).exists()


def list_event_types() -> QuerySet[TypeEvent]:
    return TypeEvent.objects.all()


def list_events(establishment_id: int) -> QuerySet[Event]:
    """Получение списка событий."""
    return (
        Event.objects.filter(establishment_id=establishment_id)
        .select_related("establishment")
        .prefetch_related("type_event")
    )

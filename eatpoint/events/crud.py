from django.db.models import QuerySet

from .models import Event, TypeEvent


def list_event_types() -> QuerySet[TypeEvent]:
    return TypeEvent.objects.all()


def list_events() -> QuerySet[Event]:
    """Получение списка событий."""
    return Event.objects.select_related("establishment").prefetch_related(
        "type_event"
    )

from django.db.models import QuerySet

from establishments.models import Establishment

from .models import Event, TypeEvent, EventPhoto


def establishment_exists(**fields) -> bool:
    """Проверка существования Заведения в базе данных."""
    return Establishment.objects.filter(**fields).exists()


def event_exists(**fields) -> bool:
    """Проверка существования События в базе данных."""
    return Event.objects.filter(**fields).exists()


def list_event_types() -> QuerySet[TypeEvent]:
    """Получение списка типов Событий"""
    return TypeEvent.objects.all()


def list_events(establishment_id: int) -> QuerySet[Event]:
    """Получение списка Событий."""
    return (
        Event.objects.filter(establishment_id=establishment_id)
        .select_related("establishment")
        .prefetch_related("type_event", "photos")
    )


def create_event(est_id: int, data: dict) -> Event:
    """Создание экземпляра События."""
    event_types = data.pop("type_event")
    event = Event.objects.create(establishment_id=est_id, **data)
    event.type_event.set(event_types)
    return event


def update_event(event: Event, data: dict) -> Event:
    """Изменение экземпляра События."""
    if "type_event" in data:
        event.type_event.clear()
        event.type_event.set(data.pop("type_event"))

    for field, value in data.items():
        if getattr(event, field):
            setattr(event, field, value)
    event.save()
    return event


def list_event_photos(event_id: int) -> QuerySet[EventPhoto]:
    """Получение списка Фото по id события."""
    return EventPhoto.objects.filter(event_id=event_id)

from datetime import date

from django.db.models import QuerySet

from establishments.models import Establishment

from .models import Event, TypeEvent, EventPhoto, RecurSetting


def establishment_exists(**fields) -> bool:
    """Проверка существования Заведения в базе данных."""
    return Establishment.objects.filter(**fields).exists()


def event_exists(**fields) -> bool:
    """Проверка существования События в базе данных."""
    return Event.objects.filter(**fields).exists()


def list_event_types() -> QuerySet[TypeEvent]:
    """Получение списка типов Событий"""
    return TypeEvent.objects.all()


def list_future_events(establishment_id: int) -> QuerySet[Event]:
    """Получение списка Событий."""
    return (
        Event.objects.filter(
            establishment_id=establishment_id,
            date_start__date__gte=date.today(),
        )
        .select_related("establishment")
        .prefetch_related("type_event", "photos")
    )


def add_event(data: dict) -> Event:
    """Создание экземпляра События."""
    return Event.objects.create(**data)


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


def create_recur_setting(
    date_start: date, date_end: date, recurrence_id: int
) -> RecurSetting:
    """Создание настроек повтора для серии событий."""
    return RecurSetting.objects.create(
        date_start=date_start, date_end=date_end, recurrence_id=recurrence_id
    )

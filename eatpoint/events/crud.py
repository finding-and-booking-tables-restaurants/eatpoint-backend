from datetime import date

from django.db.models import QuerySet

from establishments.models import Establishment

from .models import Event, TypeEvent, EventPhoto, RecurSetting, Reccurence


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


def list_event_photos(event_id: int) -> QuerySet[EventPhoto]:
    """Получение списка Фото по id события."""
    return EventPhoto.objects.filter(event_id=event_id)


def create_recur_setting(**fields) -> RecurSetting:
    """Создание настроек повтора для серии событий."""
    return RecurSetting.objects.create(**fields)


def list_recurrencies() -> QuerySet[Reccurence]:
    return Reccurence.objects.all()


def bulk_events_clear_types(start_event: Event) -> None:
    """Единовременное удаление связей Событие-Типы у серии событий."""
    Event.type_event.through.objects.filter(
        event__recur_settings=start_event.recur_settings,
        event__date_start__gte=start_event.date_start,
    ).delete()


def bulk_events_set_types(
    events: QuerySet[Event], event_types: list[TypeEvent]
) -> None:
    """Единовременное назначение типов событий списку событий."""
    event_type_relations = []
    for event in events:
        for type_event in event_types:
            event_type_relations.append(
                Event.type_event.through(
                    event_id=event.id, typeevent=type_event
                )
            )
    Event.type_event.through.objects.bulk_create(event_type_relations)


def bulk_events_clear_photos(start_event: Event) -> None:
    """Единовременное удаление связей Событие-Фото у серии событий."""
    Event.photos.through.objects.filter(
        event__recur_settings=start_event.recur_settings,
        event__date_start__gte=start_event.date_start,
    ).delete()


def bulk_events_set_photos(
    events: QuerySet[Event], photos: list[EventPhoto]
) -> None:
    """Единовременное назначение фотографий серии событий."""
    photos_relations = []
    for event in events:
        for photo in photos:
            photos_relations.append(
                Event.photos.through(event_id=event.id, eventphoto=photo)
            )
    Event.photos.through.objects.bulk_create(photos_relations)


def bulk_events_fields_update(events: QuerySet[Event], new_data: dict) -> None:
    """Единовременное обновление полей в серии событий."""
    fields = [field for field in new_data.keys()]
    for event in events:
        for field, value in new_data.items():
            if getattr(event, field):
                setattr(event, field, value)
    Event.objects.bulk_update(events, fields=fields)


def get_events_seria(event: Event) -> QuerySet[Event]:
    """Получение серии событий, начиная с переданного."""
    return Event.objects.filter(
        recur_settings=event.recur_settings, date_start__gte=event.date_start
    )

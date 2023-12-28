from datetime import timedelta

from django.db.utils import IntegrityError
from django.db.transaction import atomic

from core.exeptions import EventHasNoSeriaException, SuchEventExistsException

from .models import Event, RecurSetting
from . import crud

#========================================================
#== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ СЕРВИСОВ ПРИЛОЖЕНИЯ EVENTS ==#
#========================================================


def form_event_data(event: Event, data: dict) -> dict:
    """Формирование словаря объекта События из События и запроса."""
    return {
        "name": data.get("name", event.name),
        "establishment_id": event.establishment_id,
        "description": data.get("description", event.description),
        "cover_image": data.get("cover_image", event.cover_image),
        "date_start": data.get("date_start", event.date_start),
        "price": data.get("price", event.price),
        "photos": data.get("photos", event.photos),
        "type_event": data.get("type_event", event.type_event),
    }


def form_recur_events_dataset(
    initial_data: dict, recur_settings: RecurSetting
) -> list[dict]:
    """Формирование списка датасетов для создания серии Событий."""
    data = initial_data.copy()
    frequency = recur_settings.recurrence.days
    start_date = initial_data["date_start"]
    data["recur_settings_id"] = recur_settings.id
    dataset = []
    while start_date.date() <= recur_settings.date_end:
        data["date_start"] = start_date
        dataset.append(data.copy())
        start_date += timedelta(days=frequency)
    return dataset


def create_single_event(data: dict) -> Event:
    """Создание 1 События"""
    event_types = data.pop("type_event")
    photos = data.pop("photos", None)
    try:
        event = crud.add_event(data=data)
    except IntegrityError:
        raise SuchEventExistsException()
    else:
        event.type_event.set(event_types)
        if photos is not None:
            event.photos.set(photos)
    return event


def create_event_seria(data: dict, recur_settings: RecurSetting) -> Event:
    """Создание серии событий."""
    event_types = data.pop("type_event")
    photos = data.pop("photos", None)

    events_datasets = form_recur_events_dataset(
        initial_data=data, recur_settings=recur_settings
    )
    try:
        crud.bulk_events_create(datasets=events_datasets)
    except IntegrityError:
        raise SuchEventExistsException()
    else:
        new_events = crud.get_events_seria_by_date(
            recur_settings=recur_settings, date_start=data["date_start"]
        )

        crud.bulk_events_set_types(events=new_events, event_types=event_types)
        if photos is not None:
            crud.bulk_events_set_photos(events=new_events, photos=photos)

        return new_events[0]


#=========================================
#== ОСНОВНЫЕ СЕРВИСЫ ПРИЛОЖЕНИЯ EVENTS ==#
#=========================================


@atomic
def create_event(est_id: int, data: dict) -> Event:
    """Сервис для создания одного События или серии повторяющихся Событий."""
    recur_data = data.pop("recur_settings", None)
    data["establishment_id"] = est_id

    if recur_data is None:
        event = create_single_event(data=data)
        return event

    recur_settings = crud.create_recur_setting(**recur_data)
    return create_event_seria(data=data, recur_settings=recur_settings)


@atomic
def update_event(event: Event, data: dict) -> Event:
    """Изменение 1 экземпляра События."""

    event_types = data.pop("type_event", None)
    if event_types is not None:
        event.type_event.clear()
        event.type_event.set(event_types)

    photos = data.pop("photos", None)
    if photos is not None:
        event.photos.clear()
        event.photos.set(photos)

    for field, value in data.items():
        if getattr(event, field):
            setattr(event, field, value)

    try:
        event.save()
    except IntegrityError:
        raise SuchEventExistsException()
    else:
        return event


@atomic
def update_event_seria(event: Event, data: dict) -> Event:
    """Обновление серии Событий, начиная с указанного события."""

    if event.recur_settings is None:
        raise EventHasNoSeriaException()

    events = crud.get_events_seria_by_event(event=event)
    recur_settings_data = data.pop("recur_settings", {})
    new_date_start = data.pop("date_start", None) or event.date_start

    recur_settings_obj = event.recur_settings
    new_recurrence = recur_settings_data.get(
        "recurrence", recur_settings_obj.recurrence
    )
    new_date_end = recur_settings_data.get(
        "date_end", recur_settings_obj.date_end
    )

    # Если изменилась дата события или настройки повторения, пересоздать серию
    if (
        event.date_start != new_date_start
        or recur_settings_obj.recurrence != new_recurrence
        or recur_settings_obj.date_end != new_date_end
    ):
        recur_settings_obj.recurrence = recur_settings_data.get("recurrence")
        recur_settings_obj.date_end = new_date_end
        recur_settings_obj.save()
        event_data = form_event_data(event=event, data=data)
        events.delete()
        return create_event_seria(
            data=event_data, recur_settings=recur_settings_obj
        )

    # Иначе обновить Типы события -> Фото -> Все остальные поля кроме даты
    event_types = data.pop("type_event", None)
    if event_types is not None:
        crud.bulk_events_clear_types(start_event=event)
        crud.bulk_events_set_types(events=events, event_types=event_types)

    photos = data.pop("photos", None)
    if photos is not None:
        crud.bulk_events_clear_photos(start_event=event)
        crud.bulk_events_set_photos(events=events, photos=photos)

    crud.bulk_events_fields_update(events=events, new_data=data)

    return crud.get_events_seria_by_date(
        recur_settings=event.recur_settings, date_start=event.date_start
    )[0]


def delete_seria(event: Event) -> bool:
    """Удаление серии событий, начиная с указанного события."""

    if event.recur_settings is None:
        raise EventHasNoSeriaException()

    events = crud.get_events_seria_by_event(event=event)
    deleted, _ = events.delete()
    return deleted

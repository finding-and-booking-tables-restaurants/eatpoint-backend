from datetime import timedelta

from django.db.transaction import atomic

from .models import Event, RecurSetting
from . import crud


def form_recur_events_dataset(
    initial_data: dict, recur_settings: RecurSetting
) -> list[dict]:
    data = initial_data
    frequency = recur_settings.recurrence.days
    start_date = initial_data["date_start"]
    data["recur_settings_id"] = recur_settings.id
    dataset = []
    while start_date.date() <= recur_settings.date_end:
        data["date_start"] = start_date
        dataset.append(data.copy())
        start_date += timedelta(days=frequency)
    return dataset


@atomic
def create_event(est_id: int, data: dict) -> Event:
    """Создание экземпляра События."""
    event_types = data.pop("type_event")
    photos = data.pop("photos", None)
    recur_data = data.pop("recur_settings", None)
    data["establishment_id"] = est_id

    if recur_data is None:
        event = crud.add_event(data=data)
        event.type_event.set(event_types)
        if photos is not None:
            event.photos.set(photos)
    else:
        recur_settings = crud.create_recur_setting(**recur_data)
        events_datasets = form_recur_events_dataset(
            initial_data=data, recur_settings=recur_settings
        )

        events_to_create = [Event(**dataset) for dataset in events_datasets]
        Event.objects.bulk_create(events_to_create)

        new_events = Event.objects.filter(recur_settings=recur_settings)

        crud.bulk_events_set_types(events=new_events, event_types=event_types)
        if photos is not None:
            crud.bulk_events_set_photos(events=new_events, photos=photos)

        return None


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
    event.save()
    return event


def update_event_seria(event: Event, data: dict) -> Event:
    """Обновление серии Событий, начиная с указанного события."""

    events = crud.get_events_seria(event=event)

    recur_settings = data.pop("recur_settings", None)
    if recur_settings is not None:
        pass

    event_types = data.pop("type_event", None)
    if event_types is not None:
        crud.bulk_events_clear_types(start_event=event)
        crud.bulk_events_set_types(events=events, event_types=event_types)

    photos = data.pop("photos", None)
    if photos is not None:
        crud.bulk_events_clear_photos(start_event=event)
        crud.bulk_events_set_photos(events=events, photos=photos)

    data.pop("date_start", None)
    crud.bulk_events_fields_update(events=events, new_data=data)

    return event


def delete_seria(event: Event) -> bool:
    """Удаление серии событий, начиная с указанного события."""

    events = crud.get_events_seria(event=event)
    deleted, _ = events.delete()

    return deleted

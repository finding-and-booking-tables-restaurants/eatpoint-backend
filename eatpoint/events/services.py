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

        created_events = Event.objects.filter(recur_settings=recur_settings)

        event_type_relations = []
        for event in created_events:
            for type_event in event_types:
                event_type_relations.append(
                    Event.type_event.through(
                        event_id=event.id, typeevent=type_event
                    )
                )
        Event.type_event.through.objects.bulk_create(event_type_relations)

        if photos is not None:
            photos_relations = []
            for event in created_events:
                for photo in photos:
                    photos_relations.append(
                        Event.photos.through(
                            event_id=event.id, eventphoto=photo
                        )
                    )
            Event.photos.through.objects.bulk_create(photos_relations)

        return

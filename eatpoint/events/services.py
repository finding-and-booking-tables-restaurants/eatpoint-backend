from datetime import date

from .models import Event, RecurSetting
from .crud import add_event, create_recur_setting


def form_recur_events_dataset(
    initial_data: dict, recur_settings: RecurSetting
) -> list[dict]:
    data = initial_data
    frequency = recur_settings.recurrence.days
    start_date = recur_settings.date_start
    data["recurrence_id"] = recur_settings.id
    dataset = []
    while start_date <= recur_settings.date_end:
        data["date_start"] = start_date
        dataset.append(data)
        start_date += frequency
    return dataset


def create_event(est_id: int, data: dict) -> Event:
    """Создание экземпляра События."""
    event_types = data.pop("type_event")
    photos = data.pop("photos")
    recurrence, date_end = data.pop("recurrence"), data.pop("date_end")
    data["establishment_id"] = est_id

    if not recurrence:
        event = add_event(data=data)
        event.type_event.set(event_types)
        event.photos.set(photos)
        return event
    else:
        recur_settings = create_recur_setting(
            date_start=data.get("date_start").date,
            date_end=date_end,
            recurrence_id=recurrence,
        )
        events_datasets = form_recur_events_dataset(
            initial_data=data, recur_settings=recur_settings
        )

        events_to_create = [Event(**dataset) for dataset in events_datasets]
        Event.objects.bulk_create(events_to_create)

        created_events = Event.objects.filter(recurrence=recur_settings)

        event_type_relations = []
        photos_relations = []
        for event in created_events:
            for type_event in event_types:
                event_type_relations.append(
                    Event.type_event.through(
                        event_id=event.id, typeevent_id=type_event
                    )
                )
            for photo in photos:
                photos_relations.append(
                    Event.photos.through(
                        event_id=event.id, eventphoto_id=photo
                    )
                )

        Event.type_event.through.objects.bulk_create(event_type_relations)
        Event.photos.through.objects.bulk_create(photos_relations)

        return created_events[0]

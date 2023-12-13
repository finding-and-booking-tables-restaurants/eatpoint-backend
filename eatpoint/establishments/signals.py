from datetime import datetime, timedelta

from geopy import Nominatim

from core.constants import AVAILABLE_DAYS, INTERVAL_MINUTES, DAYS
from core.services import time_generator
from establishments.models import (
    Establishment,
    Table,
)
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from reservation.models import Slot


@receiver(pre_save, sender=Establishment)
def create_coordinates_by_address(sender, instance, **kwargs):
    geolocator = Nominatim(user_agent="Eatpoint")
    address = str(instance.address)
    city = str(instance.cities)
    full_address = city + " " + address
    location = geolocator.geocode(full_address)
    if location:
        instance.latitude, instance.longitude = (
            location.latitude,
            location.longitude,
        )


@receiver(post_save, sender=Table)
def create_slots(sender, instance, **kwargs):
    table = instance
    zone = table.zone
    establishment = zone.establishment
    start_date = datetime.now().date()
    days = AVAILABLE_DAYS

    for day in range(days):
        current_date = start_date + timedelta(days=day)

        # Проверяем, является ли текущий день рабочим для заведения
        week_day = establishment.worked.filter(
            day=DAYS[current_date.weekday()]
        )

        if week_day.exists() and not week_day.first().day_off:
            # Получаем рабочие часы заведения
            start_time = week_day.first().start
            end_time = week_day.first().end
            worked_time = time_generator(
                start_time, end_time, INTERVAL_MINUTES
            )

            # Создаем слоты для каждой половины часа в рабочие часы
            for time in worked_time:
                if table.is_active:
                    Slot.objects.get_or_create(
                        establishment=establishment,
                        zone=zone,
                        date=current_date,
                        time=time,
                        table=table,
                        seats=table.seats,
                    )

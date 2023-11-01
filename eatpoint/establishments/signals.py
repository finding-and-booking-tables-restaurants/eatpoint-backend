from datetime import datetime, timedelta
import locale

from establishments.models import (
    WorkEstablishment,
    ZoneEstablishment,
)
from django.db.models.signals import post_save
from django.dispatch import receiver

from reservation.models import Availability


@receiver(post_save, sender=WorkEstablishment)
def create_availability_work(sender, instance, created, **kwargs):
    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    establishment = instance.establishment
    start_date = datetime.now().date()
    days = 7
    zones = ZoneEstablishment.objects.filter(establishment=establishment)
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.strftime("%A").lower()
        if WorkEstablishment.objects.filter(
            establishment=establishment,
            day=day_of_week,
            day_off=False,
        ).exists():
            for zone in zones:
                Availability.objects.get_or_create(
                    zone=zone,
                    date=current_date,
                    available_seats=zone.seats,
                    establishment=establishment,
                )


@receiver(post_save, sender=ZoneEstablishment)
def create_availability_zone(sender, instance, created, **kwargs):
    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    establishment = instance.establishment
    start_date = datetime.now().date()
    days = 7
    zones = ZoneEstablishment.objects.filter(establishment=establishment)
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.strftime("%A").lower()
        if WorkEstablishment.objects.filter(
            establishment=establishment,
            day=day_of_week,
            day_off=False,
        ).exists():
            for zone in zones:
                Availability.objects.get_or_create(
                    zone=zone,
                    date=current_date,
                    available_seats=zone.seats,
                    establishment=establishment,
                )

from datetime import datetime, timedelta

from establishments.models import Establishment
from django.db.models.signals import post_save
from django.dispatch import receiver

from reservation.models import Availability


@receiver(post_save, sender=Establishment)
def create_establishment(sender, instance, created, **kwargs):
    start_date = datetime.now().date()
    days = 7
    zones = instance.zones.all()
    for day in range(days):
        current_date = start_date + timedelta(days=day)

        for zone in zones:
            if not Availability.objects.filter(
                zone=zone,
                date=current_date,
            ).exists():
                Availability.objects.create(
                    zone=zone,
                    date=current_date,
                    available_seats=zone.seats,
                )

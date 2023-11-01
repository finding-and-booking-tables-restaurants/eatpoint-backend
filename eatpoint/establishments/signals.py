from core.services import days_available
from establishments.models import (
    WorkEstablishment,
    ZoneEstablishment,
    Establishment,
)
from django.db.models.signals import post_save
from django.dispatch import receiver

from reservation.models import Availability


@receiver(post_save, sender=WorkEstablishment)
def create_availability_work(sender, instance, created, **kwargs):
    establishment = instance.establishment
    zone = ZoneEstablishment
    work = WorkEstablishment
    available = Availability
    days_available(establishment, zone, work, available)


@receiver(post_save, sender=ZoneEstablishment)
def create_availability_zone(sender, instance, created, **kwargs):
    establishment = instance.establishment
    zone = ZoneEstablishment
    work = WorkEstablishment
    available = Availability
    days_available(establishment, zone, work, available)


@receiver(post_save, sender=Establishment)
def create_availability_est(sender, instance, created, **kwargs):
    establishment = instance
    zone = ZoneEstablishment
    work = WorkEstablishment
    available = Availability
    days_available(establishment, zone, work, available)

from geopy import Nominatim

from core.services import days_available
from establishments.models import (
    WorkEstablishment,
    ZoneEstablishment,
    Establishment,
)
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from reservation.models import Availability


@receiver(post_save, sender=WorkEstablishment)
def create_availability_work(sender, instance, created, **kwargs):
    """Создает свободные слоты при создании времени работы"""
    establishment = instance.establishment
    zone = ZoneEstablishment
    work = WorkEstablishment
    available = Availability
    days_available(establishment, zone, work, available)


@receiver(post_save, sender=ZoneEstablishment)
def create_availability_zone(sender, instance, created, **kwargs):
    """Создает свободные слоты при создании зоны"""
    establishment = instance.establishment
    zone = ZoneEstablishment
    work = WorkEstablishment
    available = Availability
    days_available(establishment, zone, work, available)


@receiver(post_save, sender=Establishment)
def create_availability_est(sender, instance, created, **kwargs):
    """Создает свободные слоты при создании заведения"""
    establishment = instance
    zone = ZoneEstablishment
    work = WorkEstablishment
    available = Availability
    days_available(establishment, zone, work, available)


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

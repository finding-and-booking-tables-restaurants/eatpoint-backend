from rest_framework.validators import ValidationError
from reservation.models import Reservation, ReservationHistory
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Reservation)
def post_reservations(sender, instance, created, **kwargs):
    """Уменьшает количество свободных мест, если появилась запись о бронировании"""
    zone = instance.zone

    if zone.available_seats == 0:
        raise ValidationError({"seats": "Мест больше нет"})
    if zone.available_seats < instance.number_guests:
        raise ValidationError({"seats": "Кол-во персон больше кол-ва мест"})

    zone.available_seats -= instance.number_guests
    zone.save()


@receiver(pre_delete, sender=Reservation)
def delete_reservation(sender, instance, **kwargs):
    """Увеличивает количество свободных мест, если запись о бронировании удалена"""
    zone = instance.zone
    zone.available_seats += instance.number_guests
    if zone.available_seats > zone.seats:
        zone.available_seats = zone.seats


@receiver(pre_delete, sender=Reservation)
def move_booking_to_history(sender, instance, **kwargs):
    """Добавляет бронирование в историю"""
    ReservationHistory.objects.create(
        user=instance.user,
        first_name=instance.first_name,
        last_name=instance.last_name,
        email=instance.email,
        telephone=instance.telephone,
        establishment=instance.establishment,
        zone=instance.zone,
        number_guests=instance.number_guests,
        date_reservation=instance.date_reservation,
        start_time_reservation=instance.start_time_reservation,
        end_time_reservation=instance.end_time_reservation,
        comment=instance.comment,
        status=False,
        reservation_date=instance.reservation_date,
    )

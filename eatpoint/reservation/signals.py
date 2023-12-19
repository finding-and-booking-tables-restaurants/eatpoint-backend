from reservation.models import Reservation, ReservationHistory, Availability
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Reservation)
def reservation_status_changed(sender, instance, **kwargs):
    """Добавляет бронирование в историю"""
    if instance._state.adding:
        # Если это новая запись, то ничего не делаем
        return None

    old_reservation = Reservation.objects.get(id=instance.id)
    slots = ",\n".join([str(slot) for slot in instance.slots.all()])

    if (
        old_reservation.is_visited != instance.is_visited
        and instance.is_visited is True
    ):
        ReservationHistory.objects.create(
            reservation_date=instance.reservation_date,
            establishment=instance.establishment,
            date_reservation=instance.date_reservation,
            start_time_reservation=instance.start_time_reservation,
            is_accepted=instance.is_accepted,
            is_visited=instance.is_visited,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            telephone=instance.telephone,
            slots=slots,
            comment=instance.comment,
            reminder_one_day=instance.reminder_one_day,
            reminder_three_hours=instance.reminder_three_hours,
            reminder_half_on_hour=instance.reminder_half_on_hour,
        )


@receiver(pre_save, sender=Reservation)
def post_reservations(sender, instance, **kwargs):
    """Уменьшает количество свободных мест, если появилась запись о бронировании"""

    availability = Availability.objects.filter(
        zone=instance.zone, date=instance.date_reservation
    ).first()
    if availability:
        if instance.number_guests <= availability.available_seats:
            availability.available_seats -= instance.number_guests
            availability.save()


@receiver(pre_delete, sender=Reservation)
def delete_reservation(sender, instance, **kwargs):
    """Увеличивает количество свободных мест, если запись о бронировании удалена"""
    zone = instance.zone
    availability = Availability.objects.filter(
        zone=zone, date=instance.date_reservation
    ).first()
    availability.available_seats += instance.number_guests
    if availability.available_seats > zone.seats:
        availability.available_seats = zone.seats
    availability.save()


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

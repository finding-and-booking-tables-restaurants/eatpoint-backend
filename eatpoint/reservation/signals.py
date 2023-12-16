from django.db.models.signals import pre_save
from django.dispatch import receiver

from reservation.models import Reservation, ReservationHistory


@receiver(pre_save, sender=Reservation)
def reservation_status_changed(sender, instance, **kwargs):
    """Добавляет бронирование в историю"""
    if instance._state.adding:
        # Если это новая запись, то ничего не делаем
        return None

    old_reservation = Reservation.objects.get(id=instance.id)

    if old_reservation.is_visited != instance.is_visited:
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
            slots=instance.slots,
            comment=instance.comment,
            reminder_one_day=instance.reminder_one_day,
            reminder_three_hours=instance.reminder_three_hours,
            reminder_half_on_hour=instance.reminder_half_on_hour,
        )

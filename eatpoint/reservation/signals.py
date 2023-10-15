from rest_framework.validators import ValidationError
import locale
from establishments.models import WorkEstablishment
from reservation.models import Reservation
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=Reservation)
def post_reservations(sender, instance, created, **kwargs):
    zone = instance.zone

    if zone.available_seats == 0:
        raise ValidationError({"seats": "Мест больше нет"})
    if zone.available_seats < instance.number_guests:
        raise ValidationError({"seats": "Кол-во персон больше кол-ва мест"})

    zone.available_seats -= instance.number_guests
    zone.save()


@receiver(pre_delete, sender=Reservation)
def delete_reservation(sender, instance, **kwargs):
    zone = instance.zone
    zone.available_seats += instance.number_guests
    if zone.available_seats > zone.seats:
        zone.available_seats = zone.seats


@receiver(pre_save, sender=Reservation)
def validate_booking_time(sender, instance, **kwargs):
    locale.setlocale(locale.LC_ALL, "ru")
    day_of_week = instance.date_reservation.strftime("%A").lower()
    working_hours = WorkEstablishment.objects.filter(
        establishment=instance.establishment,
        day=day_of_week,
        day_off=False,
    )
    res_start = instance.start_time_reservation
    res_end = instance.end_time_reservation
    working_hours_est = WorkEstablishment.objects.get(day=day_of_week)
    start = working_hours_est.start
    end = working_hours_est.end

    if start > end:
        raise ValidationError(
            "Время начала бронирования не может быть больше конца"
        )
    if not working_hours:
        raise ValidationError("Заведение не работает в указанный день недели")
    if not (start <= res_start <= end and start <= res_end <= end):
        raise ValidationError(
            "Бронирование возможно только в часы работы заведения"
        )


# @receiver(post_save, sender=Reservation)
# def move_booking_to_history(sender, instance, **kwargs):
#     now = timezone.now()
#     end_reservation = datetime.strptime(instance.end_time_reservation, "%H:%M").time()
#     res_end = datetime.combine(instance.date_reservation, end_reservation)
#     print(now)
#     print(res_end)
#     if res_end < now:
#         print('aboba')
#         ReservationHistory.objects.create(
#             user=instance.user,
#             first_name = instance.first_name,
#             last_name = instance.last_name,
#             email = instance.email,
#             telephone = instance.telephone,
#             establishment = instance.establishment,
#             zone = instance.zone,
#             number_guests = instance.number_guests,
#             date_reservation = instance.date_reservation,
#             start_time_reservation = instance.start_time_reservation,
#             end_time_reservation = instance.end_time_reservation,
#             comment = instance.comment,
#             status=False,
#         )
#         instance.delete()

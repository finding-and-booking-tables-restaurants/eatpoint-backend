from datetime import datetime, timedelta

import pytz
from celery import shared_task, current_app
from django.conf import settings as django_settings
from django.core.mail import send_mail
from django.db import transaction

from core.constants import AVAILABLE_DAYS, DAYS, INTERVAL_MINUTES
from core.services import time_generator
from establishments.models import Table
from reservation.models import Reservation, Slot, ReservationHistory

tz_moscow = pytz.timezone(django_settings.CELERY_TIMEZONE)


@shared_task()
def send_reminder(booking_id: int, for_client: bool = False):
    try:
        booking = Reservation.objects.get(id=booking_id)
        subj = (
            "Подтвердите бронирование"
            if not for_client
            else "Напоминание о бронировании"
        )
        context = (
            f"телефон: {booking.telephone}"
            if not for_client
            else f"адрес: {booking.establishment.address}"
        )
        recipient_email = (
            booking.establishment.email if not for_client else booking.email
        )
        slot = booking.slots.first()
        message = f"""
            {subj}:
            заведение: {booking.establishment},
            {context},
            дата: {booking.date_reservation},
            время: {booking.start_time_reservation},
            зона: {slot.table.zone},
            гостей: {slot.table.seats}
        """

        send_mail(
            subject=subj,
            message=message,
            from_email=django_settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
        )
        return message

    except Reservation.DoesNotExist:
        return None


@shared_task
def check_unconfirmed_booking():
    try:
        bookings = Reservation.objects.filter(
            is_accepted=False, is_deleted=False
        )
        for booking in bookings:
            booking_data = booking.date_reservation
            booking_time = datetime.strptime(
                booking.start_time_reservation, "%H:%M"
            ).time()
            booking_date_time = datetime.combine(booking_data, booking_time)
            if (
                not booking.is_accepted
                and booking_date_time > datetime.now()
                and not is_task_scheduled(send_reminder, booking.id, None)
            ):
                send_reminder.apply_async(
                    args=[booking.id], kwargs={"for_client": False}
                )

    except Reservation.DoesNotExist:
        return None


@shared_task
def find_bookings_with_remind():
    """Поиск броней с напоминанием."""
    try:
        bookings = Reservation.objects.filter(
            is_accepted=True, is_deleted=False
        )
    except Reservation.DoesNotExist:
        return "Подтвержденных броней не найдено"

    for booking in bookings:
        booking_data = booking.date_reservation
        booking_time = datetime.strptime(
            booking.start_time_reservation, "%H:%M"
        ).time()
        booking_date_time = datetime.combine(booking_data, booking_time)
        time_now_iso = (datetime.now() - timedelta(minutes=1)).isoformat()

        # За 30 минут до начала
        reminder_time = booking_date_time - timedelta(minutes=30)
        reminder_time = tz_moscow.localize(reminder_time).isoformat()
        if (
            not is_task_scheduled(send_reminder, booking.id, reminder_time)
            and booking.reminder_half_on_hour
            and reminder_time > time_now_iso
        ):
            send_reminder.apply_async(
                args=[booking.id],
                kwargs={"for_client": True},
                eta=reminder_time,
            )

        # За 3 часа до начала
        reminder_time = booking_date_time - timedelta(hours=3)
        reminder_time = tz_moscow.localize(reminder_time).isoformat()
        if (
            not is_task_scheduled(send_reminder, booking.id, reminder_time)
            and booking.reminder_three_hours
            and reminder_time > time_now_iso
        ):
            send_reminder.apply_async(
                args=[booking.id],
                kwargs={"for_client": True},
                eta=reminder_time,
            )

        # За 1 день до начала
        reminder_time = booking_date_time - timedelta(days=1)
        reminder_time = tz_moscow.localize(reminder_time).isoformat()
        if (
            not is_task_scheduled(send_reminder, booking.id, reminder_time)
            and booking.reminder_one_day is True
            and reminder_time > time_now_iso
        ):
            send_reminder.apply_async(
                args=[booking.id],
                kwargs={"for_client": True},
                eta=reminder_time,
            )


def is_task_scheduled(task, booking_id, reminder_time):
    scheduled_tasks = current_app.control.inspect().scheduled()
    for tasks in scheduled_tasks.values():
        for scheduled_task in tasks:
            if (
                scheduled_task["request"]["name"] == task.name
                and scheduled_task["request"]["args"] == [booking_id]
                and scheduled_task["eta"] == reminder_time
            ):
                return True
    return False


@shared_task
def delete_old_slots():
    """Удаление слотов с датой меньше сегодняшней."""
    Slot.objects.filter(date__lt=datetime.now().date()).delete()
    return "Слоты далее сегодняшней даты удалены"


@shared_task
def create_slots():
    """Создание слотов."""
    start_date = datetime.now().date()
    days = AVAILABLE_DAYS

    with transaction.atomic():
        tables = Table.objects.filter(
            establishment__is_verified=True, is_active=True
        ).prefetch_related("zone__establishment")

        for table in tables:
            establishment = table.zone.establishment

            for day in range(days):
                current_date = start_date + timedelta(days=day)
                week_day = establishment.worked.filter(
                    day=DAYS[current_date.weekday()]
                )

                if week_day.exists() and not week_day.first().day_off:
                    start_time = week_day.first().start
                    end_time = week_day.first().end
                    worked_time = time_generator(
                        start_time, end_time, INTERVAL_MINUTES
                    )

                    for time in worked_time:
                        if table.is_active:
                            Slot.objects.get_or_create(
                                establishment=establishment,
                                zone=table.zone,
                                date=current_date,
                                time=time,
                                table=table,
                                seats=table.seats,
                            )
    return "Новые слоты созданы"


@shared_task
def copy_reservation_to_archive_after_visit():
    """Копирование бронирования в архив после посещения"""
    subj = None
    reservations = Reservation.objects.filter(
        is_accepted=True, is_visited=True, is_deleted=False
    ).prefetch_related("slots")
    for reservation in reservations:
        slots = ";\n".join([str(slot) for slot in reservation.slots.all()])

        try:
            ReservationHistory.objects.get(reservation_id=reservation.id)
        except ReservationHistory.DoesNotExist:
            ReservationHistory.objects.create(
                reservation_date=reservation.reservation_date,
                reservation_id=reservation.id,
                establishment=reservation.establishment,
                date_reservation=reservation.date_reservation,
                start_time_reservation=reservation.start_time_reservation,
                is_accepted=reservation.is_accepted,
                is_visited=reservation.is_visited,
                first_name=reservation.first_name,
                last_name=reservation.last_name,
                email=reservation.email,
                telephone=reservation.telephone,
                slots=slots,
                comment=reservation.comment,
                reminder_one_day=reservation.reminder_one_day,
                reminder_three_hours=reservation.reminder_three_hours,
                reminder_half_on_hour=reservation.reminder_half_on_hour,
            )
            subj = "Исполненные брони скопированы в архив"
    return subj


@shared_task
def delete_reservation_after_visit():
    """Удаление бронирования исполненные (более 30 дней назад)"""

    reservations = Reservation.objects.filter(
        is_accepted=True,
        is_visited=True,
        date_reservation__lt=(datetime.now().date() - timedelta(days=30)),
    )
    subj = None
    for reservation in reservations:
        try:
            ReservationHistory.objects.get(reservation_id=reservation.id)
            reservation.delete()
        except ReservationHistory.DoesNotExist:
            continue
        else:
            subj = "Исполненные (более 30 дней назад) брони удалены"
    return subj


@shared_task
def delete_rejected_reservation():
    """Удаление отмененных бронирований (выполняется каждое 1 число)"""

    reservations = Reservation.objects.filter(
        is_deleted=True,
        date_reservation__lt=(datetime.now().date()),
    )
    subj = None
    for reservation in reservations:
        try:
            ReservationHistory.objects.get(reservation_id=reservation.id)
            reservation.delete()
        except ReservationHistory.DoesNotExist:
            continue
        else:
            subj = "Отменённые брони (более 30 дней назад) удалены"
    return subj

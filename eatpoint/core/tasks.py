from datetime import datetime, timedelta

import pytz
from celery import shared_task, current_app
from django.conf import settings as django_settings
from django.core.mail import send_mail

from reservation.models import Reservation

tz_moscow = pytz.timezone(django_settings.CELERY_TIMEZONE)


@shared_task()
def send_reminder(_id, for_client=False):
    try:
        if for_client:
            booking = Reservation.objects.get(id=_id, status=True)
            subj = "Напоминание о бронировании"
            context = f"адрес: {booking.establishment.address}"
        else:
            booking = Reservation.objects.get(id=_id, status=False)
            subj = "Подтвердите бронирование"
            context = f"телефон: {booking.telephone}"

        message = (
            f"{subj}: \n"
            f"заведение: {booking.establishment}, \n"
            f"{context}, \n"
            f"дата: {booking.date_reservation}, \n"
            f"время: {booking.start_time_reservation}, \n"
            f"зона: {booking.zone}, \n"
            f"гостей: {booking.number_guests}"
        )

        # asyncio.run(send_code(message))
        send_mail(
            subject=subj,
            message=message,
            from_email=django_settings.EMAIL_HOST_USER,
            recipient_list=[
                booking.email or booking.user.email,
            ],
        )
        return message

    except Reservation.DoesNotExist:
        return None


@shared_task
def send_message_for_confirm_booking():
    try:
        bookings = Reservation.objects.filter(status=False)
        for booking in bookings:
            if not booking.status:
                send_reminder.apply_async(
                    args=[booking.id], kwargs={"for_client": False}
                )
    except Reservation.DoesNotExist:
        return None


@shared_task
def check_bookings():
    try:
        bookings = Reservation.objects.filter(status=True)
    except Reservation.DoesNotExist:
        return "Подтвержденных броней не найдено"

    for booking in bookings:
        booking_data = booking.date_reservation
        booking_time = booking.start_time_reservation.split(":")
        booking_date_time = datetime(
            year=booking_data.year,
            month=booking_data.month,
            day=booking_data.day,
            hour=int(booking_time[0]),
            minute=int(booking_time[1]),
        )

        # За 30 минут до начала
        reminder_time = booking_date_time - timedelta(minutes=30)
        reminder_time = tz_moscow.localize(reminder_time).isoformat()
        if (
            not is_task_scheduled(send_reminder, booking.id, reminder_time)
            and booking.reminder_half_on_hour is True
            and reminder_time >= datetime.now().isoformat()
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
            and booking.reminder_three_hours is True
            and reminder_time >= datetime.now().isoformat()
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
            and reminder_time >= datetime.now().isoformat()
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

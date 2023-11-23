import asyncio
from datetime import datetime

from celery import shared_task

from .tgbot import send_code
from reservation.models import Reservation


@shared_task
def bar():
    return "Hello World!"


@shared_task
def send_message_for_confirm_booking_by_id(_id):
    booking = Reservation.objects.get(id=_id)
    message = (
        f"Подтвердите бронирование: \n"
        f"заведение: {booking.establishment}, \n"
        f"телефон: {booking.telephone}, \n"
        f"дата: {booking.date_reservation}, \n"
        f"время: {booking.start_time_reservation}, \n"
        f"зона: {booking.zone}, \n"
        f"гостей:{booking.number_guests}, \n"
    )
    asyncio.run(send_code(message))


@shared_task
def send_message_for_confirm_booking():
    bookings = Reservation.objects.filter(status=False)
    for booking in bookings:
        if not booking.status:
            send_message_for_confirm_booking_by_id.delay(booking.id)


@shared_task
def send_reminder_one_day():
    # reminder_half_on_hour
    bookings_by_reminder_one_day = Reservation.objects.filter(
        status=True, reminder_one_day=True
    )
    for booking in bookings_by_reminder_one_day:
        booking_data = booking.date_reservation
        booking_time = booking.start_time_reservation
        data_string = booking_data + " " + booking_time
        date_format = "%d-%m-%Y %H:%M:%S"
        target_datetime = datetime.strptime(
            data_string, date_format
        ) - datetime.timedelta(days=1)
        send_message_for_confirm_booking_by_id.apply_async(
            args=[booking.id], eta=target_datetime
        )


def send_reminder_three_hours():
    bookings_by_reminder_three_hours = Reservation.objects.filter(
        status=True, reminder_three_hours=True
    )
    for booking in bookings_by_reminder_three_hours:
        booking_data = booking.date_reservation
        booking_time = booking.start_time_reservation
        data_string = booking_data + " " + booking_time
        date_format = "%d-%m-%Y %H:%M:%S"
        target_datetime = datetime.strptime(
            data_string, date_format
        ) - datetime.timedelta(hours=3)
        send_message_for_confirm_booking_by_id.apply_async(
            args=[booking.id], eta=target_datetime
        )

import asyncio

from celery import shared_task

from .tgbot import send_code
from reservation.models import Reservation


@shared_task
def bar():
    return "Hello World!"


@shared_task
def send_message_for_confirm_booking():
    bookings = Reservation.objects.filter(status=False)
    for booking in bookings:
        if not booking.status:
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

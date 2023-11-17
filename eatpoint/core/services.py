from datetime import datetime, timedelta
import random
import locale


from core.constants import (
    INTERVAL_MINUTES,
    START_TIME,
    END_TIME,
    MIN_LIMIT_RESERVATION_CODE,
    MAX_LIMIT_RESERVATION_CODE,
)


def time_generator():
    """Выводит списко времени с заданым интервалом"""
    start_time = datetime.strptime(START_TIME, "%H:%M")
    end_time = datetime.strptime(END_TIME, "%H:%M")
    time_list = []

    current_time = start_time
    while current_time <= end_time:
        time_list.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=INTERVAL_MINUTES)
    return time_list


def choices_generator(data: list):
    """Генерирует choices из списка"""
    return [(item, item) for item in data]


def generate_reservation_code():
    """Генерация кода подтверждения"""
    random.seed()
    return str(
        random.randint(
            MIN_LIMIT_RESERVATION_CODE,
            MAX_LIMIT_RESERVATION_CODE,
        )
    )


def days_available(establishment, zone, work, available):
    """Создает свободные дни"""
    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    start_date = datetime.now().date()
    days = 30
    zones = zone.objects.filter(establishment=establishment)
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.strftime("%A").lower()
        if work.objects.filter(
            establishment=establishment,
            day=day_of_week,
            day_off=False,
        ).exists():
            for zone in zones:
                available.objects.get_or_create(
                    zone=zone,
                    date=current_date,
                    available_seats=zone.seats,
                    establishment=establishment,
                )

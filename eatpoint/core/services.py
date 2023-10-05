from datetime import datetime, timedelta

from core.constants import INTERVAL_MINUTES


def time_generator():
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    time_list = []

    current_time = start_time
    while current_time < end_time:
        time_list.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=INTERVAL_MINUTES)
    return time_list


def choices_generator(data: list):
    return [(item, item) for item in data]

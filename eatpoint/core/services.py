from datetime import datetime, timedelta

from core.constants import INTERVAL_MINUTES, START_TIME, END_TIME


def time_generator():
    """Выводит списко времени с заданым интервалом"""
    start_time = datetime.strptime(START_TIME, "%H:%M")
    end_time = datetime.strptime(END_TIME, "%H:%M")
    time_list = []

    current_time = start_time
    while current_time < end_time:
        time_list.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=INTERVAL_MINUTES)
    return time_list


def choices_generator(data: list):
    """Генерирует choices из списка"""
    return [(item, item) for item in data]

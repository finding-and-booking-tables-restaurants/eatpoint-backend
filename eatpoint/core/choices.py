from core.constants import CHECKS, DAYS, ADMINISTRATOR
from core.services import choices_generator, time_generator
from core.constants import (
    CLIENT,
    RESTORATEUR,
    SMS,
    EMAIL,
    TELEGRAM,
    NOTHING,
    INTERVAL_MINUTES,
    START_TIME,
    END_TIME,
)

# Выбор времени с интервалом 30 мин
TIME_CHOICES = choices_generator(
    time_generator(START_TIME, END_TIME, INTERVAL_MINUTES)
)

# Выбор среднего чека
CHECK_CHOICES = choices_generator(CHECKS)

# Выбор дня недели
DAY_CHOICES = choices_generator(DAYS)

# Выбор роли
ROLE_CHOICES = (
    (CLIENT, "Клиент"),
    (RESTORATEUR, "Ресторатор"),
    (ADMINISTRATOR, "Админ_ресторана"),
)

# Выбор способа отправки кода подтверждения
SEND_CONFIRM_CODE_METHOD = (
    (SMS, "СМС"),
    (EMAIL, "эл. почта"),
    (TELEGRAM, "Телеграм"),
    (NOTHING, "не отправлять"),
)


RESERVATION_STATUS = (
    ("is_accepted", "подтверждена"),
    ("is_visited", "посещена"),
    ("is_deleted", "удалена"),
)

from core.constants import CHECKS
from core.services import choices_generator, time_generator
from core.constants import CLIENT, RESTORATEUR, SMS, EMAIL, TELEGRAM, NOTHING

TIME_CHOICES = choices_generator(time_generator())
CHECK_CHOICES = choices_generator(CHECKS)

ROLE_CHOICES = (
    (CLIENT, "Клиент"),
    (RESTORATEUR, "Ресторатор"),
)

SEND_CONFIRM_CODE_METHOD = (
    (SMS, "СМС"),
    (EMAIL, "эл. почта"),
    (TELEGRAM, "Телеграм"),
    (NOTHING, "не отправлять"),
)
DAY_CHOICES = [
    ("monday", "понедельник"),
    ("tuesday", "вторник"),
    ("wednesday", "среда"),
    ("thursday", "четверг"),
    ("friday", "пятница"),
    ("saturday", "суббота"),
    ("sunday", "воскресенье"),
]

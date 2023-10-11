from core.constants import DAYS, CHECKS
from core.services import choices_generator, time_generator
from core.constants import CLIENT, RESTORATEUR, SMS, EMAIL, TELEGRAM, NOTHING

TIME_CHOICES = choices_generator(time_generator())
CHECK_CHOICES = choices_generator(CHECKS)
DAY_CHOICES = choices_generator(DAYS)

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

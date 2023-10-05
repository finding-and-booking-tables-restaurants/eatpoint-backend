from core.constants import DAYS, CHECKS
from core.services import choices_generator, time_generator


TIME_CHOICES = choices_generator(time_generator())
CHECK_CHOICES = choices_generator(CHECKS)
DAY_CHOICES = choices_generator(DAYS)

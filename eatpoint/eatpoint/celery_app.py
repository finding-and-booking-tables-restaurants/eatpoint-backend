import os

import django
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eatpoint.settings")
django.setup()

app = Celery("eatpoint")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # "send-message-every-4-minutes": {
    #     "task": "core.tasks.send_message_for_confirm_booking",
    #     "schedule": crontab(minute="*/4"),
    # },
    "check_bookings_task": {
        "task": "core.tasks.check_bookings",
        "schedule": crontab(minute="*/30"),
    },
}

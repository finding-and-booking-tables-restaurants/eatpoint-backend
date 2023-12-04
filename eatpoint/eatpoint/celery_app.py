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
    "send-reminder-for-confirm-booking": {
        "task": "core.tasks.send_message_for_confirm_booking",
        "schedule": crontab(hour="*", minute="1, 3, 5, 8, 13, 21, 34"),
    },
    "check_bookings_task": {
        "task": "core.tasks.check_bookings",
        "schedule": crontab(minute="*/30"),
    },
}

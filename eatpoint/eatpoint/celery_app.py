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
    "check_unconfirmed_bookings": {
        "task": "core.tasks.check_unconfirmed_booking",
        "schedule": crontab(minute="*/1"),
    },
    "send_reminder_for_client": {
        "task": "core.tasks.find_bookings_with_remind",
        "schedule": crontab(minute="*/15"),
    },
    "create_slots": {
        "task": "core.tasks.create_slots",
        "schedule": crontab(hour=0, minute=1),
    },
    "delete_old_slots": {
        "task": "core.tasks.delete_old_slots",
        "schedule": crontab(hour=0, minute=5),
    },
    "copy_reservations_to_archive": {
        "task": "core.tasks.copy_reservations_to_archive",
        "schedule": crontab(minute="*/15"),
    },
    "delete_reservations_after_visit": {
        "task": "core.tasks.delete_reservations_after_visit",
        "schedule": crontab(minute="*/20"),
    },
}

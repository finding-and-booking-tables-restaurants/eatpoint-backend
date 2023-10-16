from django.contrib import admin
from .models import Reservation, ReservationHistory


# Register your models here.


@admin.register(ReservationHistory)
class ReservationHistory(admin.ModelAdmin):
    """Админка: история бронирования"""

    list_display = (
        "id",
        "user",
    )


@admin.register(Reservation)
class EstablishmentReservAdmin(admin.ModelAdmin):
    """Админка: бронирования"""

    list_display = (
        "id",
        "user",
        "email",
        "telephone",
        "establishment",
        "number_guests",
        "date_reservation",
        "start_time_reservation",
        "end_time_reservation",
        "comment",
        "reminder_one_day",
        "reminder_three_hours",
        "reminder_half_on_hour",
    )
    list_filter = (
        "id",
        "user",
        "establishment",
        "date_reservation",
        "start_time_reservation",
    )
    empty_value_display = "-пусто-"

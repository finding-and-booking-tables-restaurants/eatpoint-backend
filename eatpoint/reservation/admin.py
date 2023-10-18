from django.contrib import admin
from .models import Reservation, ReservationHistory


@admin.register(ReservationHistory)
class ReservationHistory(admin.ModelAdmin):
    """Админка: история бронирования"""

    list_display = (
        "id",
        "email",
        "telephone",
        "establishment",
        "zone",
        "number_guests",
        "date_reservation",
        "start_time_reservation",
        "status",
    )
    list_filter = (
        "establishment",
        "date_reservation",
    )
    empty_value_display = "-пусто-"


@admin.register(Reservation)
class EstablishmentReservAdmin(admin.ModelAdmin):
    """Админка: бронирования"""

    list_display = (
        "reservation_date",
        "id",
        "email",
        "telephone",
        "establishment",
        "zone",
        "number_guests",
        "date_reservation",
        "start_time_reservation",
        "status",
    )
    list_filter = (
        "establishment",
        "date_reservation",
    )
    empty_value_display = "-пусто-"

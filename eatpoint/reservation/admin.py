from django.contrib import admin

from .models import (
    Reservation,
    ReservationHistory,
    ConfirmationCode,
)


@admin.register(ConfirmationCode)
class ConfirmationCode(admin.ModelAdmin):
    """Админка: код подтверждения для анонинов"""

    list_display = (
        "email",
        "code",
        "is_verified",
    )


@admin.register(ReservationHistory)
class ReservationHistory(admin.ModelAdmin):
    """Админка: история бронирования"""

    list_display = (
        "id",
        "establishment",
        "date_reservation",
        "start_time_reservation",
        "is_visited",
        "email",
        "telephone",
        "last_name",
        "first_name",
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
        "establishment",
        "date_reservation",
        "start_time_reservation",
        "user",
        "email",
        "telephone",
        "last_name",
        "first_name",
        "is_accepted",
        "is_visited",
        "reminder_one_day",
        "reminder_three_hours",
        "reminder_half_on_hour",
    )
    list_filter = (
        "reservation_date",
        "is_accepted",
        "is_visited",
    )
    search_fields = (
        "last_name",
        "first_name",
        "telephone",
        "email",
        "date_reservation",
        "user",
    )
    empty_value_display = "-пусто-"
    fieldsets = (
        ("Статус бронирования", {"fields": ("is_accepted", "is_visited")}),
        ("Ресторан", {"fields": ("establishment",)}),
        (
            "Основная информация о клиенте",
            {"fields": ("user",)},
        ),
        (
            "Контакты клиента",
            {"fields": ("first_name", "last_name", "telephone", "email")},
        ),
        (
            "Бронирование",
            {"fields": ("slots",)},
        ),
        ("Комментарии к бронированию", {"fields": ("comment",)}),
        (
            "Напоминания",
            {
                "fields": (
                    "reminder_one_day",
                    "reminder_three_hours",
                    "reminder_half_on_hour",
                )
            },
        ),
    )

from django.contrib import admin

from .models import (
    Reservation,
    ReservationHistory,
    ConfirmationCode,
)


@admin.register(ConfirmationCode)
class ConfirmationCode(admin.ModelAdmin):
    """Админка: история бронирования"""

    list_display = (
        "id",
        "email",
        "code",
        "is_verified",
    )


@admin.register(ReservationHistory)
class ReservationHistory(admin.ModelAdmin):
    """Админка: история бронирования"""

    list_display = (
        "id",
        "reservation_id",
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
class ReservationAdmin(admin.ModelAdmin):
    """Админка: бронирования"""

    raw_id_fields = ("slots",)

    list_display = (
        "id",
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
        "is_deleted",
        "reminder_one_day",
        "reminder_three_hours",
        "reminder_half_on_hour",
    )
    list_filter = (
        "reservation_date",
        "is_accepted",
        "is_visited",
        "is_deleted",
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
        (
            "Статус бронирования",
            {"fields": ("is_accepted", "is_visited", "is_deleted")},
        ),
        ("Ресторан", {"fields": ("establishment",)}),
        (
            "Основная информация о клиенте",
            {"fields": ("user",)},
        ),
        (
            "Контакты не зарегистрированного пользователя",
            {"fields": ("first_name", "last_name", "telephone", "email")},
        ),
        (
            "Бронирование",
            {
                "fields": (
                    "date_reservation",
                    "start_time_reservation",
                    "slots",
                )
            },
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

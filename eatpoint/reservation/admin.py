from django.contrib import admin
from django import forms

from .models import (
    Reservation,
    ReservationHistory,
    Availability,
    ConfirmationCode,
)


@admin.register(ConfirmationCode)
class ConfirmationCode(admin.ModelAdmin):
    """Админка: история бронирования"""


@admin.register(Availability)
class AvailabilityHistory(admin.ModelAdmin):
    """Админка: свободные места"""

    list_display = (
        "id",
        "date",
        "zone",
        "available_seats",
    )


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


class YourModelAdminForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"


@admin.register(Reservation)
class EstablishmentReservAdmin(admin.ModelAdmin):
    """Админка: бронирования"""

    form = YourModelAdminForm
    list_display = (
        "reservation_date",
        "user",
        "email",
        "telephone",
        "last_name",
        "first_name",
        "status",
        "reminder_one_day",
        "reminder_three_hours",
        "reminder_half_on_hour",
    )
    list_filter = (
        "reservation_date",
        "status",
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
        ("Статус бронирования", {"fields": ("status",)}),
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
            {
                "fields": (
                    "slots",
                    "comment",
                )
            },
        ),
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

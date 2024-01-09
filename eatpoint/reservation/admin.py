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


class YourModelAdminForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        zone = cleaned_data.get("zone")
        date = cleaned_data.get("date_reservation")
        availability = Availability.objects.get(zone=zone, date=date)
        print(availability.available_seats)
        if availability == 0:
            raise forms.ValidationError(
                "Количество мест не может быть равно 0."
            )
        return cleaned_data


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Админка: бронирования"""

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

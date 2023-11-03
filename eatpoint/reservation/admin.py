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
class EstablishmentReservAdmin(admin.ModelAdmin):
    """Админка: бронирования"""

    form = YourModelAdminForm
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

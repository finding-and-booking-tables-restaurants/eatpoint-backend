from rest_framework import serializers

from core.choices import RESERVATION_STATUS
from establishments.models import ZoneEstablishment, Establishment
from reservation.models import (
    Reservation,
    ReservationHistory,
    Slot,
)


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ("id",)


class ReservationsUnregUserSerializer(serializers.ModelSerializer):
    """Сериализация данных:
    форма бронирования для не авторизованного пользователя"""

    slots = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Slot.objects.all()
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "slots",
            "first_name",
            "last_name",
            "email",
            "telephone",
            "comment",
            "date_reservation",
            "start_time_reservation",
            "establishment",
            "reminder_one_day",
            "reminder_three_hours",
            "reminder_half_on_hour",
        )


class ReservationsUserSerializer(serializers.ModelSerializer):
    """Сериализация данных:
    форма бронирования для авторизованного пользователя"""

    slots = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Slot.objects.all()
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "date_reservation",
            "start_time_reservation",
            "establishment",
            "slots",
            "comment",
            "reminder_one_day",
            "reminder_three_hours",
            "reminder_half_on_hour",
        )


class UpdateReservationActionSerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(required=True, choices=RESERVATION_STATUS)

    class Meta:
        model = Reservation
        fields = ["action"]


class ReservationsHistoryEditSerializer(serializers.ModelSerializer):
    """История бронирования"""

    class Meta:
        model = ReservationHistory
        fields = (
            "establishment",
            "comment",
            "email",
        )


class ZoneReservationsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneEstablishment
        fields = (
            "zone",
        )


class SpecialEstablishmentSerializer(serializers.ModelSerializer):
    """Сериализация данных: Заведение(короткий)"""

    class Meta:
        model = Establishment
        fields = [
            "id",
            "name",
            "poster",
            "address",
        ]


class SpecialSlotSerializer(serializers.ModelSerializer):
    """Сериализация данных: Слот"""

    table = serializers.StringRelatedField(source="table.number")
    zone = serializers.StringRelatedField(source="zone.zone")

    class Meta:
        model = Slot
        fields = (
            "id",
            "date",
            "time",
            "zone",
            "table",
            "seats",
        )


class ReservationsUserListSerializer(serializers.ModelSerializer):
    """Пользователь"""

    establishment = SpecialEstablishmentSerializer()
    slots = SpecialSlotSerializer(many=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
            "is_accepted",
            "is_visited",
            "is_deleted",
            "slots",
        )


class ReservationsRestorateurListSerializer(serializers.ModelSerializer):
    """Ресторатор"""

    establishment = serializers.CharField(source="establishment.name")
    slots = SpecialSlotSerializer(many=True)
    user = serializers.StringRelatedField(source="user.name")

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
            "date_reservation",
            "start_time_reservation",
            "user",
            "first_name",
            "last_name",
            "email",
            "telephone",
            "slots",
            "comment",
            "reminder_one_day",
            "reminder_three_hours",
            "reminder_half_on_hour",
            "is_accepted",
            "is_visited",
            "is_deleted",
        )


class ReservationsUpdateUserSerializer(serializers.ModelSerializer):
    """Ресторатор"""

    slots = SpecialSlotSerializer(many=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "date_reservation",
            "start_time_reservation",
            "slots",
            "comment",
            "reminder_one_day",
            "reminder_three_hours",
            "reminder_half_on_hour",
            "is_deleted",
        )


class AvailableSlotsSerializer(serializers.ModelSerializer):
    """Свободные слоты"""

    establishment = serializers.CharField(source="establishment__name")
    zone = serializers.CharField(source="zone__zone")
    table = serializers.CharField(source="table__number")
    seats = serializers.CharField(source="table__seats")

    class Meta:
        model = Slot
        fields = (
            "id",
            "date",
            "time",
            "establishment",
            "zone",
            "table",
            "seats",
        )

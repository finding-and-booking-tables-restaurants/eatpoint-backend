from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class UpdateReservationStatusSerializer(serializers.ModelSerializer):
    is_accepted = serializers.BooleanField(required=True)

    class Meta:
        model = Reservation
        fields = ["is_accepted"]

    def validate(self, validated_data):
        if validated_data.get("is_accepted") is None:
            raise ValidationError(
                {
                    "status": "Отправь '{is_accepted: True}' "
                    "для подтверждения посещения заведения!"
                }
            )
        return validated_data


class UpdateReservationVisitedSerializer(serializers.ModelSerializer):
    is_visited = serializers.BooleanField(required=True)

    class Meta:
        model = Reservation
        fields = ["is_visited"]

    def validate(self, validated_data):
        if validated_data.get("is_visited") is None:
            raise ValidationError(
                {
                    "status": "Отправь '{is_visited: True}' "
                    "для подтверждения посещения заведения!"
                }
            )
        return validated_data


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
            "seats",
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


class ReservationsUserListSerializer(serializers.ModelSerializer):
    """Пользователь"""

    slots = serializers.StringRelatedField()
    establishment = SpecialEstablishmentSerializer()

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
            "is_accepted",
            "is_visited",
            "slots",
        )


class ReservationsRestorateurListSerializer(serializers.ModelSerializer):
    """Ресторатор"""

    establishment = serializers.CharField(source="establishment.name")
    # zone = serializers.CharField(source="zone.zone")

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
            "first_name",
            "email",
            "telephone",
            "slots",
            "comment",
            "reminder_one_day",
            "reminder_three_hours",
            "reminder_half_on_hour",
            "is_accepted",
            "is_visited",
        )


class AvailableSlotsSerializer(serializers.ModelSerializer):
    """Свободные слоты"""

    establishment = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    zone = serializers.SlugRelatedField(
        slug_field="zone",
        read_only=True,
    )
    table = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Slot
        fields = (
            "id",
            "date",
            "time",
            "establishment",
            "zone",
            "table",
        )

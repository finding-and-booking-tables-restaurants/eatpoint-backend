from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from establishments.models import ZoneEstablishment, Establishment
from reservation.models import (
    Reservation,
    ReservationHistory,
    Availability,
    Slot,
)


class ReservationsEditSerializer(serializers.ModelSerializer):
    """Сериализация данных: форма бронирования для не авторизованного пользователя"""

    class Meta:
        model = Reservation
        fields = (
            "id",
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
        )

    def validate(self, validated_data):
        # establishment = self.context["request"].parser_context["kwargs"][
        #     "establishment_id"
        # ]
        # date = validated_data.get("date_reservation")
        return validated_data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["zone"] = str(instance.zone)
        return representation


class UpdateReservationStatusSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(required=True)

    class Meta:
        model = Reservation
        fields = ["status"]

    def validate(self, validated_data):
        if validated_data.get("status") is None:
            raise ValidationError(
                {"status": "Введите ture для подтверждения бронирования!"}
            )
        return validated_data


class ReservationsHistoryEditSerializer(serializers.ModelSerializer):
    """История бронирования"""

    class Meta:
        model = ReservationHistory
        fields = (
            "establishment",
            "comment",
            # "zone",
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

    # zone = serializers.StringRelatedField()
    establishment = SpecialEstablishmentSerializer()

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
            "status",
            # "zone",
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
            "comment",
            "reminder_one_day",
            "reminder_three_hours",
            "reminder_half_on_hour",
            # "zone",
            "status",
        )


class AvailableSlotsSerializer(serializers.ModelSerializer):
    """Свободные слоты"""

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


class AvailabilitySerializer(serializers.ModelSerializer):
    """Свободные места на день"""

    zone = serializers.CharField(source="zone.zone")

    class Meta:
        model = Availability
        fields = (
            "id",
            "zone",
            "date",
            "available_seats",
        )


class DateAvailabilitySerializer(serializers.ModelSerializer):
    """Сериализатор свободных слотов"""

    class Meta:
        model = Slot
        fields = ("date",)


@extend_schema_field(OpenApiTypes.TIME)
class TimeAvailabilitySerializer(serializers.Serializer):
    """Сериализатор свободных дат и времени для зоны"""

    time = serializers.TimeField(format="%H:%M")

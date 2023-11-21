from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.validators import (
    string_validator,
    validate_seats,
    validate_reservation_time_zone,
    validated_available_seats,
)
from establishments.models import ZoneEstablishment, Establishment
from reservation.models import Reservation, ReservationHistory, Availability


class ReservationsEditSerializer(serializers.ModelSerializer):
    """Сериализация данных: форма бронирования для не авторизованного пользователя"""

    establishment = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    user = serializers.SlugRelatedField(
        slug_field="id",
        read_only=True,
    )
    telephone = PhoneNumberField(
        help_text="Номер телефона",
        required=False,
    )
    first_name = serializers.CharField(
        required=False, help_text="Имя", validators=[string_validator]
    )
    email = serializers.EmailField(
        help_text="Почта",
        required=False,
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
            "first_name",
            "email",
            "telephone",
            "number_guests",
            "date_reservation",
            "start_time_reservation",
            "comment",
            "reminder_one_day",
            "reminder_three_hours",
            "reminder_half_on_hour",
            "user",
            "zone",
        )

    def validate(self, validated_data):
        establishment = self.context["request"].parser_context["kwargs"][
            "establishment_id"
        ]
        number_guests = validated_data.get("number_guests")
        zone = validated_data.get("zone")
        date = validated_data.get("date_reservation")
        available_seats = validated_available_seats(zone, date)
        validate_seats(available_seats.available_seats, number_guests)
        validate_reservation_time_zone(validated_data, establishment)
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
            "number_guests",
            "date_reservation",
            "start_time_reservation",
            "comment",
            "zone",
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

    zone = serializers.StringRelatedField()
    establishment = SpecialEstablishmentSerializer()

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
            "number_guests",
            "date_reservation",
            "start_time_reservation",
            "status",
            "zone",
        )


class ReservationsRestorateurListSerializer(serializers.ModelSerializer):
    """Ресторатор"""

    establishment = serializers.CharField(source="establishment.name")
    zone = serializers.CharField(source="zone.zone")

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
            "first_name",
            "email",
            "telephone",
            "number_guests",
            "date_reservation",
            "start_time_reservation",
            "comment",
            "reminder_one_day",
            "reminder_three_hours",
            "reminder_half_on_hour",
            "zone",
            "status",
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
    """Сериализатор свободных дат и времени для зоны"""

    class Meta:
        model = Availability
        fields = ("date",)


@extend_schema_field(OpenApiTypes.TIME)
class TimeAvailabilitySerializer(serializers.Serializer):
    """Сериализатор свободных дат и времени для зоны"""

    time = serializers.TimeField(format="%H:%M")

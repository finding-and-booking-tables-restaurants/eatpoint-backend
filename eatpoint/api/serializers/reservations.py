from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from core.validators import (
    validate_reserv_anonim,
    string_validator,
)
from establishments.models import ZoneEstablishment, Establishment
from reservation.models import Reservation, ReservationHistory


class AuthReservationsEditSerializer(serializers.ModelSerializer):
    """Сериализация данных: форма бронирования для авторизованного пользователя"""

    establishment = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    user = serializers.SlugRelatedField(
        slug_field="id",
        read_only=True,
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
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
        user = self.context["request"].user
        validate_reserv_anonim(user, validated_data)
        return validated_data


class ReservationsHistoryEditSerializer(serializers.ModelSerializer):
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
    zone = serializers.SerializerMethodField(source="zone__name")
    establishment = SpecialEstablishmentSerializer()

    class Meta:
        model = Reservation
        fields = (
            "establishment",
            "number_guests",
            "date_reservation",
            "start_time_reservation",
            "zone",
        )


class ReservationsRestorateurListSerializer(serializers.ModelSerializer):
    zone = serializers.SerializerMethodField(source="zone__name")
    establishment = serializers.SerializerMethodField(
        source="establishment__name"
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
            "zone",
        )

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from core.validators import validate_reserv_anonim
from reservation.models import Reservation


class ReservationsEditSerializer(serializers.ModelSerializer):
    establishment = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    user = serializers.SlugRelatedField(
        slug_field="id",
        read_only=True,
    )
    telephone = PhoneNumberField(required=False)
    last_name = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "establishment",
            "first_name",
            "last_name",
            "email",
            "telephone",
            "number_guests",
            "date_reservation",
            "start_time_reservation",
            "end_time_reservation",
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

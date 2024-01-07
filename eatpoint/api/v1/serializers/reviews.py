from rest_framework import serializers
from reviews.models import OwnerResponse, Review
from users.models import User


class SmallUserSerializer(serializers.ModelSerializer):
    """Сериализация данных: Данные пользователя для отзывов"""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "role",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация данных: Отзывы"""

    establishment = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    author = SmallUserSerializer(read_only=True)
    response = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"
        model = Review

    def get_response(self, obj):
        owner_response = obj.owner_responses.first()
        if owner_response:
            return OwnerResponseSerializer(owner_response).data
        else:
            return None

    def validate(self, data):
        """Проверка на уникальность отзыва"""
        if self.context["request"].method == "POST":
            establishment = self.context["view"].kwargs.get("establishment_id")
            user = self.context["request"].user

            is_booking_confirmed = user.reservationhistory.filter(
                establishment=establishment, status=True
            ).exists()
            if not is_booking_confirmed:
                raise serializers.ValidationError(
                    "Отзыв недоступен из-за отсутствия подтвержденной брони"
                )

            if Review.objects.filter(
                author=user, establishment=establishment
            ).exists():
                raise serializers.ValidationError(
                    "Нельзя оставить повторный отзыв на одно заведение"
                )
        return data


class OwnerResponseSerializer(serializers.ModelSerializer):
    """
    Сериализация данных: Ответ владельца заведения на отзыв.
    Для получения информации о самом отзыве в ответе API при
    создании ответа владельца на отзыв, добавлен 'review'.
    """

    class Meta:
        model = OwnerResponse
        fields = ["id", "text", "created"]

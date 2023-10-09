from django.db.models import Avg
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_field,
)
from rest_framework import serializers

from establishments.models import (
    Establishment,
    WorkEstablishment,
    Kitchen,
    ZoneEstablishment,
    Favorite,
    Review,
    Service,
    SocialEstablishment,
    ImageEstablishment,
    Type,
)
from users.models import User


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = [
            "id",
            "name",
            "description",
            "slug",
        ]


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = [
            "id",
            "name",
            "description",
            "slug",
        ]


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "description",
            "slug",
        ]


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialEstablishment
        fields = [
            "id",
            "name",
        ]


class ZoneEstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneEstablishment
        fields = [
            "id",
            "zone",
            "seats",
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageEstablishment
        fields = [
            "id",
            "name",
            "image",
        ]


class WorkEstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkEstablishment
        fields = [
            "day",
            "start",
            "end",
            "day_off",
        ]


# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = "__all__"


# class TableEstablishmentSerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(source="table.id")
#     name = serializers.ReadOnlyField(source="table.name")
#     description = serializers.ReadOnlyField(source="table.description")
#     slug = serializers.ReadOnlyField(source="table.slug")
#
#     class Meta:
#         model = ZoneEstablishment
#         fields = [
#             "id",
#             "name",
#             "description",
#             "slug",
#             "seats",
#             "status",
#         ]


class EstablishmentSerializer(serializers.ModelSerializer):
    kitchen = KitchenSerializer(read_only=True, many=True)
    type = TypeSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    services = ServicesSerializer(read_only=True, many=True)
    social = SocialSerializer(read_only=True, many=True)
    image = ImageSerializer(read_only=True, many=True)
    zone = ZoneEstablishmentSerializer(read_only=True, many=True)
    work = WorkEstablishmentSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField("get_rating")

    class Meta:
        fields = [
            "id",
            "owner",
            "name",
            "type",
            "city",
            "address",
            "kitchen",
            "services",
            "zone",
            "average_check",
            "poster",
            "email",
            "telephone",
            "description",
            "is_verified",
            "work",
            "is_favorited",
            "social",
            "image",
            "rating",
        ]
        model = Establishment

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_favorited(self, obj):
        request = self.context.get("request")
        user = request.user
        if request is None or user.is_anonymous:
            return False
        return Favorite.objects.filter(establishment=obj, user=user).exists()

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_rating(self, obj):
        return Review.objects.filter(establishment=obj).aggregate(
            Avg("score")
        )["score__avg"]


class SmallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "role",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    establishment = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    author = SmallUserSerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = Review

    def validate(self, data):
        if self.context["request"].method == "POST":
            if Review.objects.filter(
                author=self.context["request"].user,
                establishment=self.context["view"].kwargs.get(
                    "establishment_id"
                ),
            ).exists():
                raise serializers.ValidationError(
                    "Нельзя оставить повторный отзыв на одно заведение"
                )
        return data

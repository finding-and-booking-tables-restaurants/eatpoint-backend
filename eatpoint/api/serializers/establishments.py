from django.db.models import Avg
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_field,
)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from core.validators import validate_uniq, file_size
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
    TypeEst,
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


class TypeEstSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEst
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
    image = Base64ImageField()
    name = serializers.CharField()

    class Meta:
        model = ImageEstablishment
        fields = [
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
#         model = zone
#         fields = [
#             "id",
#             "name",
#             "description",
#             "slug",
#             "seats",
#             "status",
#         ]


class EstablishmentSerializer(serializers.ModelSerializer):
    kitchens = KitchenSerializer(read_only=True, many=True)
    types = TypeEstSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    services = ServicesSerializer(read_only=True, many=True)
    socials = SocialSerializer(read_only=True, many=True)
    image = ImageSerializer(read_only=True, many=True)
    zones = ZoneEstablishmentSerializer(read_only=True, many=True)
    worked = WorkEstablishmentSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField("get_rating")
    poster = Base64ImageField()

    class Meta:
        fields = [
            "id",
            "owner",
            "name",
            "types",
            "city",
            "address",
            "kitchens",
            "services",
            "zones",
            "average_check",
            "poster",
            "email",
            "telephone",
            "description",
            "is_verified",
            "worked",
            "is_favorited",
            "socials",
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


class EstablishmentEditSerializer(serializers.ModelSerializer):
    poster = Base64ImageField(
        max_length=None,
        use_url=True,
    )
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    images = ImageSerializer(
        many=True,
        help_text="Несколько изображений",
    )
    worked = WorkEstablishmentSerializer(
        many=True,
        help_text="Время работы",
    )
    zones = ZoneEstablishmentSerializer(
        many=True,
        help_text="Зоны заведения",
    )
    socials = SocialSerializer(
        many=True,
        help_text="Соц. сети",
    )

    class Meta:
        model = Establishment
        fields = [
            "id",
            "owner",
            "name",
            "types",
            "city",
            "address",
            "kitchens",
            "services",
            "zones",
            "average_check",
            "poster",
            "email",
            "telephone",
            "description",
            "worked",
            "socials",
            "images",
        ]

    def validate_image(self, image):
        file_size(image)
        return image

    def __create_image(self, images, establishment):
        for image in images:
            ImageEstablishment.objects.bulk_create(
                [
                    ImageEstablishment(
                        establishment=establishment,
                        image=image.get("image"),
                        name=image.get("name"),
                    )
                ]
            )

    def __create_work(self, worked, establishment):
        for work in worked:
            WorkEstablishment.objects.bulk_create(
                [
                    WorkEstablishment(
                        establishment=establishment,
                        day=work.get("day"),
                        day_off=work.get("day_off"),
                        start=work.get("start"),
                        end=work.get("end"),
                    )
                ]
            )

    def __create_zone(self, zones, establishment):
        for zone in zones:
            ZoneEstablishment.objects.bulk_create(
                [
                    ZoneEstablishment(
                        establishment=establishment,
                        zone=zone.get("zone"),
                        seats=zone.get("seats"),
                    )
                ]
            )

    def __create_social(self, socials, establishment):
        for social in socials:
            SocialEstablishment.objects.bulk_create(
                [
                    SocialEstablishment(
                        establishment=establishment,
                        name=social.get("name"),
                    )
                ]
            )

    def create(self, validated_data):
        images = validated_data.pop("images")
        worked = validated_data.pop("worked")
        zones = validated_data.pop("zones")
        socials = validated_data.pop("socials")
        kitchens = validated_data.pop("kitchens")
        types = validated_data.pop("types")
        services = validated_data.pop("services")
        establishment = Establishment.objects.create(**validated_data)
        establishment.kitchens.set(kitchens)
        establishment.types.set(types)
        establishment.services.set(services)
        self.__create_image(images, establishment)
        self.__create_work(worked, establishment)
        self.__create_zone(zones, establishment)
        self.__create_social(socials, establishment)
        return establishment

    def validate(self, data):
        worked = data.get("worked")
        field = "day"
        validate_uniq(worked, field)
        return data


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


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Establishment.objects.all(),
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = Establishment
        fields = ["establishment", "user"]


class SpecialEstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = [
            "id",
            "name",
            "poster",
            "description",
        ]

from django.db.models import Avg
from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_field,
)


from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from core.choices import DAY_CHOICES
from core.validators import validate_uniq, file_size, validate_count
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
    City,
)
from users.models import User


class KitchenSerializer(serializers.ModelSerializer):
    """Сериализация данных: Кухня"""

    lookup_field = "name"

    class Meta:
        model = Kitchen
        fields = [
            "id",
            "name",
            "description",
            "slug",
        ]


class CitySerializer(serializers.ModelSerializer):
    """Сериализация данных: Города"""

    lookup_field = "name"

    class Meta:
        model = City
        fields = [
            "name",
        ]


class TypeEstSerializer(serializers.ModelSerializer):
    """Сериализация данных: Тип заведения"""

    lookup_field = "name"

    class Meta:
        model = TypeEst
        fields = [
            "id",
            "name",
            "description",
            "slug",
        ]


class ServicesSerializer(serializers.ModelSerializer):
    """Сериализация данных: Доп. Услуги"""

    lookup_field = "name"

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "description",
            "slug",
        ]


class SocialSerializer(serializers.ModelSerializer):
    """Сериализация данных: Соц. сети"""

    name = serializers.URLField(required=False)

    class Meta:
        model = SocialEstablishment
        fields = [
            "name",
        ]


class ZoneEstablishmentSerializer(serializers.ModelSerializer):
    """Сериализация данных: Зоны заведения"""

    available_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = ZoneEstablishment
        fields = [
            "id",
            "zone",
            "seats",
            "available_seats",
        ]


class ImageSerializer(serializers.ModelSerializer):
    """Сериализация данных: Изображения заведения"""

    image = Base64ImageField()
    name = serializers.CharField(required=False)

    class Meta:
        model = ImageEstablishment
        fields = [
            "name",
            "image",
        ]


class WorkEstablishmentSerializer(serializers.ModelSerializer):
    """Сериализация данных: Время работы"""

    day = serializers.ChoiceField(
        choices=DAY_CHOICES,
    )

    class Meta:
        model = WorkEstablishment
        fields = [
            "day",
            "start",
            "end",
            "day_off",
        ]

    def to_representation(self, instance):
        """Отображение выходного дня"""
        data = super().to_representation(instance)
        if instance.day_off:
            data["day_off_st"] = "Выходной"
            data.pop("start", None)
            data.pop("end", None)
        return data


# class EventSerializer(serializers.ModelSerializer):
#     """Сериализация данных: События"""
#     class Meta:
#         model = Event
#         fields = "__all__"


class EstablishmentSerializer(serializers.ModelSerializer):
    """Сериализация данных: Заведение"""

    kitchens = KitchenSerializer(read_only=True, many=True)
    types = TypeEstSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    services = ServicesSerializer(read_only=True, many=True)
    socials = SocialSerializer(read_only=True, many=True)
    images = ImageSerializer(read_only=True, many=True)
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
            "cities",
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
            "images",
            "rating",
        ]
        model = Establishment

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_favorited(self, obj):
        """Отображение заведения в избранном"""
        request = self.context.get("request")
        user = request.user
        if request is None or user.is_anonymous:
            return False
        return Favorite.objects.filter(establishment=obj, user=user).exists()

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_rating(self, obj):
        """Отображение среднего рейтинга заведения"""
        return Review.objects.filter(establishment=obj).aggregate(
            Avg("score")
        )["score__avg"]


class KitchenListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return KitchenSerializer(value).data


class TypeListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return TypeEstSerializer(value).data


class ServiceListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return ServicesSerializer(value).data


class CityListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return CitySerializer(value).data


class EstablishmentEditSerializer(serializers.ModelSerializer):
    """Сериализация данных(запись): Заведение"""

    poster = Base64ImageField()
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    images = ImageSerializer(
        many=True,
        help_text="Несколько изображений",
        required=False,
        default=None,
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
        required=False,
        default=None,
    )
    telephone = PhoneNumberField(
        help_text="Номер телефона",
    )
    cities = CityListField(slug_field="name", queryset=City.objects.all())
    kitchens = KitchenListField(
        slug_field="name", queryset=Kitchen.objects.all(), many=True
    )
    types = TypeListField(
        slug_field="name", queryset=TypeEst.objects.all(), many=True
    )
    services = ServiceListField(
        slug_field="name", queryset=Service.objects.all(), many=True
    )

    class Meta:
        model = Establishment
        fields = [
            "id",
            "owner",
            "name",
            "types",
            "cities",
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

    def __create_image(self, images, establishment):
        """Создание картинки"""
        if images is not None:
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
        """Создание времени работы"""
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
        """Создание зоны"""
        for zone in zones:
            ZoneEstablishment.objects.bulk_create(
                [
                    ZoneEstablishment(
                        establishment=establishment,
                        zone=zone.get("zone"),
                        seats=zone.get("seats"),
                        available_seats=zone.get("seats"),
                    )
                ]
            )

    def __create_social(self, socials, establishment):
        """Создание соц.сетей"""
        if socials is not None:
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
        """Проверка на уникальность поля day"""
        images = data.get("images")
        poster = data.get("poster")
        worked = data.get("worked")
        field = "day"
        file_size(poster)
        validate_count(images)
        for image in images:
            file_size(image.get("image"))
        validate_uniq(worked, field)
        return data


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

    class Meta:
        fields = "__all__"
        model = Review

    def validate(self, data):
        """Проверка на уникальность отзыва"""
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
    """Сериализация данных: Избранное"""

    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Establishment.objects.all(),
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = Establishment
        fields = ["establishment", "user"]

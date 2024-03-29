from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_field,
)

from rest_framework import serializers

from core.choices import DAY_CHOICES
from core.services import days_available
from core.validators import validate_uniq
from establishments.models import (
    Establishment,
    WorkEstablishment,
    Kitchen,
    ZoneEstablishment,
    Service,
    SocialEstablishment,
    ImageEstablishment,
    TypeEst,
    City,
)


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
            "slug",
        ]


class TypeEstSerializer(serializers.ModelSerializer):
    """Сериализация данных: Тип заведения"""

    lookup_field = "name"
    name = serializers.CharField(required=True)

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

    name = serializers.CharField(required=True)
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

    class Meta:
        model = ZoneEstablishment
        fields = [
            "id",
            "zone",
            "seats",
        ]


class ImageSerializer(serializers.ModelSerializer):
    """Сериализация данных: Изображения заведения"""

    image = serializers.ImageField()
    name = serializers.CharField(required=False, default="Изображение")

    class Meta:
        model = ImageEstablishment
        fields = [
            "id",
            "image",
            "name",
        ]


class WorkEstablishmentSerializer(serializers.ModelSerializer):
    """Сериализация данных: Время работы"""

    day = serializers.ChoiceField(
        choices=DAY_CHOICES,
        required=True,
    )
    day_off = serializers.BooleanField(default=False)

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


class CityListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return value.name


class KitchenListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return value.name


class TypeListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return value.name


class ServiceListField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return value.name


class SocialField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return value.name


class PosterEditSerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(required=True)

    class Meta:
        model = Establishment
        fields = ("poster",)


class ZoneSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneEstablishment
        fields = ("zone", "seats")


class EstablishmentSerializer(serializers.ModelSerializer):
    """Сериализация данных: Заведение"""

    owner = serializers.CharField(source="email")
    types = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    cities = serializers.CharField(source="cities.name")
    images = ImageSerializer(many=True)
    kitchens = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    services = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    zones = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="zone",
    )
    socials = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    worked = WorkEstablishmentSerializer(
        many=True,
        help_text="Время работы",
    )
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    rating = serializers.SerializerMethodField("get_rating")
    review_count = serializers.SerializerMethodField("get_review_count")

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
            "is_verified",
            "worked",
            "is_favorited",
            "socials",
            "images",
            "rating",
            "review_count",
        ]

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_favorited(self, instance):
        """Отображение заведения в избранном"""
        request = self.context.get("request")
        user = request.user
        if request is None or user.is_anonymous:
            return False
        return instance.favorite.filter(user=user).exists()

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_rating(self, instance):
        """Отображение среднего рейтинга заведения"""
        return instance.rating

    @extend_schema_field(OpenApiTypes.INT)
    def get_review_count(self, instance):
        """Отображение количества отзывов заведения"""
        return instance.review_count


class EstablishmentEditSerializer(serializers.ModelSerializer):
    """Сериализация данных(запись): Заведение"""

    owner = serializers.CharField(source="email")
    types = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    cities = serializers.CharField(source="cities.name")
    kitchens = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    services = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    zones = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="zone",
    )
    socials = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    worked = WorkEstablishmentSerializer(
        many=True,
        help_text="Время работы",
    )

    class Meta:
        model = Establishment
        fields = [
            "id",
            "poster",
            "owner",
            "name",
            "types",
            "cities",
            "address",
            "kitchens",
            "services",
            "zones",
            "average_check",
            "email",
            "telephone",
            "description",
            "worked",
            "socials",
        ]

    def validate(self, data):
        """Проверка на уникальность поля day"""
        worked = data.get("worked")
        field = "day"
        validate_uniq(worked, field)
        return data

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
                    ),
                ]
            )

    def __create_availavle(self, establishment):
        days_available(establishment, ZoneEstablishment, WorkEstablishment)

    def __create_social(self, socials, establishment):
        """Создание соц.сетей"""
        if socials is not None:
            for social in socials:
                SocialEstablishment.objects.bulk_create(
                    [
                        SocialEstablishment(
                            establishment=establishment,
                            name=social,
                        )
                    ]
                )

    def create(self, validated_data):
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
        self.__create_work(worked, establishment)
        self.__create_zone(zones, establishment)
        self.__create_social(socials, establishment)
        self.__create_availavle(establishment)
        return establishment

    def update(self, instance, validated_data):
        if "worked" in validated_data:
            worked = validated_data.pop("worked")
            WorkEstablishment.objects.filter(establishment=instance).delete()
            instance.worked.clear()
            self.__create_work(worked, instance)
        if "zones" in validated_data:
            zones = validated_data.pop("zones")
            ZoneEstablishment.objects.filter(establishment=instance).delete()
            instance.zones.clear()
            self.__create_zone(zones, instance)
        if "socials" in validated_data:
            socials = validated_data.pop("socials")
            SocialEstablishment.objects.filter(establishment=instance).delete()
            instance.socials.clear()
            self.__create_social(socials, instance)
        if "kitchens" in validated_data:
            instance.kitchens.set(validated_data.pop("kitchens"))
        if "types" in validated_data:
            instance.types.set(validated_data.pop("types"))
        if "services" in validated_data:
            instance.services.set(validated_data.pop("services"))
        self.__create_availavle(instance)

        return super().update(
            instance,
            validated_data,
        )

    def to_representation(self, instance):
        return EstablishmentSerializer(
            instance,
            context={"request": self.context.get("request")},
        ).data

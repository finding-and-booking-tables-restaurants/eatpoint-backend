from django.db.models import Avg
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_field,
)


from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from core.choices import DAY_CHOICES
from core.services import days_available
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
from reservation.models import Availability
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
        return CitySerializer(value).data


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

    poster = serializers.ImageField()
    owner = serializers.CharField(source="owner.email")
    kitchens = KitchenListField(
        slug_field="name",
        queryset=Kitchen.objects.all(),
        many=True,
    )
    types = TypeListField(
        slug_field="name",
        queryset=TypeEst.objects.all(),
        many=True,
    )
    services = ServiceListField(
        slug_field="name",
        queryset=Service.objects.all(),
        many=True,
    )
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    images = ImageSerializer(many=True)
    worked = WorkEstablishmentSerializer(
        many=True,
        help_text="Время работы",
    )
    zones = ZoneEstablishmentSerializer(many=True)
    socials = SocialField(
        slug_field="name",
        queryset=SocialEstablishment.objects.all(),
        many=True,
    )
    rating = serializers.SerializerMethodField("get_rating")
    cities = serializers.CharField(source="cities.name")
    review_count = serializers.SerializerMethodField("get_review_count")

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
            "review_count",
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

    @extend_schema_field(OpenApiTypes.INT)
    def get_review_count(self, obj):
        """Отображение количества отзывов заведения"""
        return Review.objects.filter(establishment=obj).count()


class EstablishmentEditSerializer(serializers.ModelSerializer):
    """Сериализация данных(запись): Заведение"""

    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    worked = WorkEstablishmentSerializer(
        many=True,
        help_text="Время работы",
    )
    zones = ZoneEstablishmentSerializer(
        many=True,
        help_text="Зоны заведения",
    )
    socials = serializers.ListField(required=False)
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
            "email",
            "telephone",
            "description",
            "worked",
            "socials",
        ]

    # def validate(self, data):
    #     """Проверка на уникальность поля day"""
    #     poster = data.get("poster")
    #     worked = data.get("worked")
    #     field = "day"
    #     validate_uniq(worked, field)
    #     file_size(poster)
    #     return data

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
        days_available(
            establishment, ZoneEstablishment, WorkEstablishment, Availability
        )

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

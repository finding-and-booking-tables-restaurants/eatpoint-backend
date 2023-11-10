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


@extend_schema_field(OpenApiTypes.BYTE)
class ImageSerializer(serializers.ModelSerializer):
    """Сериализация данных: Изображения заведения"""

    # image = serializers.ImageField()
    # name = serializers.CharField(required=False, default="Изображение")

    class Meta:
        model = ImageEstablishment
        fields = [
            "image",
            "name",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            return data.get("image")


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


class ImageField(serializers.SlugRelatedField):
    def to_representation(self, value):
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(value.image.url)
        return super().to_representation(value)


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
    images = ImageField(
        slug_field="image",
        queryset=ImageEstablishment.objects.all(),
        many=True,
    )
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
    zones = ZoneEstablishmentSerializer(many=True, required=True)
    poster = serializers.ImageField()
    socials = serializers.ListField(
        child=serializers.CharField(),
        required=False,
    )
    telephone = PhoneNumberField(
        help_text="Номер телефона",
        required=True,
    )
    cities = CityListField(
        required=True, slug_field="name", queryset=City.objects.all()
    )
    kitchens = serializers.ListField(
        child=serializers.CharField(),
        required=True,
    )
    types = serializers.ListField(
        child=serializers.CharField(),
        required=True,
    )
    services = serializers.ListField(
        child=serializers.CharField(),
        required=True,
    )
    images = ImageSerializer(many=True, read_only=True)

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
            "images",
            "poster",
        ]

    def validate(self, data):
        """
        Валидация данных при изменении.
        """
        if "types" not in data:
            raise serializers.ValidationError(
                "Типы заведения обязательны при изменении."
            )
        return data

    # def validate(self, data):
    #     """Проверка на уникальность поля day"""
    #     worked = data.get("worked")
    #     field = "day"
    #     validate_uniq(worked, field)
    #
    #     return data

    # def validate_poster(self, value):
    #
    #     return value

    def __create_work(self, worked, establishment):
        """Создание времени работы"""
        for work in worked:
            WorkEstablishment.objects.bulk_create(
                [
                    WorkEstablishment(
                        establishment=establishment,
                        **work,
                    )
                ]
            )

    def __create_zone(self, zones, establishment):
        """Создание зоны"""
        for zone in zones:
            ZoneEstablishment.objects.bulk_create(
                [
                    ZoneEstablishment(establishment=establishment, **zone),
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
        worked = validated_data.pop("worked", [])
        zones = validated_data.pop("zones", [])
        socials = validated_data.pop("socials")
        kitchens = validated_data.pop("kitchens", [])
        types = validated_data.pop("types", [])
        services = validated_data.pop("services", [])

        establishment = Establishment.objects.create(**validated_data)

        establishment.kitchens.set(Kitchen.objects.filter(name__in=kitchens))
        establishment.types.set(TypeEst.objects.filter(name__in=types))
        establishment.services.set(Service.objects.filter(name__in=services))
        self.__create_work(worked, establishment)
        self.__create_zone(zones, establishment)
        self.__create_social(socials, establishment)
        self.__create_availavle(establishment)
        return establishment

    def update(self, instance, validated_data):
        worked = validated_data.pop("worked")
        WorkEstablishment.objects.filter(establishment=instance).delete()
        instance.worked.clear()
        self.__create_work(worked, instance)
        zones = validated_data.pop("zones", [])
        ZoneEstablishment.objects.filter(establishment=instance).delete()
        instance.zones.clear()
        self.__create_zone(zones, instance)
        socials = validated_data.pop("socials")
        SocialEstablishment.objects.filter(establishment=instance).delete()
        instance.socials.clear()
        self.__create_social(socials, instance)
        self.__create_availavle(instance)

        kitchens = validated_data.pop("kitchens", [])
        types = validated_data.pop("types", [])
        services = validated_data.pop("services", [])
        instance.kitchens.clear()
        instance.types.clear()
        instance.services.clear()
        instance.kitchens.set(Kitchen.objects.filter(name__in=kitchens))
        instance.types.set(TypeEst.objects.filter(name__in=types))
        instance.services.set(Service.objects.filter(name__in=services))

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

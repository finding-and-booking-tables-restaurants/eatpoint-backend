from drf_spectacular.utils import (
    extend_schema_field,
)
from rest_framework import serializers

from establishments.models import (
    Establishment,
    WorkEstablishment,
    Kitchen,
    Work,
    TableEstablishment,
    Favorite,
    Event,
    Review,
)
from users.models import User


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = [
            "id",
            "name",
            "description",
            "slug",
        ]


class WorkEstablishmentSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(
        source="order_dt.name",
    )
    start = serializers.TimeField(
        source="order_dt.start",
        format="%I:%M",
    )
    end = serializers.TimeField(
        source="order_dt.end",
        format="%I:%M",
    )

    class Meta:
        model = WorkEstablishment
        fields = [
            "name",
            "start",
            "end",
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class TableEstablishmentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="table.id")
    name = serializers.ReadOnlyField(source="table.name")
    description = serializers.ReadOnlyField(source="table.description")
    slug = serializers.ReadOnlyField(source="table.slug")

    class Meta:
        model = TableEstablishment
        fields = [
            "id",
            "name",
            "description",
            "slug",
            "seats",
            "status",
        ]


class EstablishmentSerializer(serializers.ModelSerializer):
    worked = serializers.SerializerMethodField("get_work")
    kitchen = KitchenSerializer(read_only=True, many=True)
    tables = serializers.SerializerMethodField("get_table")
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    event = serializers.SerializerMethodField("get_event")

    class Meta:
        fields = "__all__"
        model = Establishment

    @extend_schema_field(WorkSerializer(many=True))
    def get_work(self, obj):
        order_dt = WorkEstablishment.objects.filter(establishment=obj)
        return WorkEstablishmentSerializer(order_dt, many=True).data

    @extend_schema_field(TableEstablishmentSerializer(many=True))
    def get_table(self, obj):
        table = TableEstablishment.objects.filter(establishment=obj)
        return TableEstablishmentSerializer(table, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        user = request.user
        if request is None or user.is_anonymous:
            return False
        return Favorite.objects.filter(establishment=obj, user=user).exists()

    @extend_schema_field(EventSerializer(many=True))
    def get_event(self, obj):
        event = Event.objects.filter(establishment=obj)
        return EventSerializer(event, many=True).data


class UserListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f"({value.first_name} {value.last_name} {value.role})"


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

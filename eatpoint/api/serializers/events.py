from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from events.models import Event, TypeEvent


class BaseTypeEventSerializer(serializers.ModelSerializer):
    """Базовый сериализатор полей Типов событий."""

    class Meta:
        model = TypeEvent
        fields = ("id", "name")


class ListTypeEventSerializer(BaseTypeEventSerializer):
    """Cериализатор полей Типов событий для списков."""

    pass


class RetrieveTypeEventSerializer(BaseTypeEventSerializer):
    """Сериализатор полей Типов событий для 1 экземпляра."""

    class Meta(BaseTypeEventSerializer.Meta):
        fields = BaseTypeEventSerializer.Meta.fields + ("description", "slug")


class BaseEventSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Событий."""

    image = Base64ImageField()

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "establishment",
            "image",
            "date_start",
            "price",
            "type_event",
        )


class ListEventSerializer(BaseEventSerializer):
    """Сериализатор для списков Событий."""

    pass


class RetrieveEventSrializer(BaseEventSerializer):
    """Сериализато Событий для 1 экземпляра."""

    class Meta(BaseEventSerializer.Meta):
        fields = BaseEventSerializer.Meta.fields + ("description", "date_end")


# class EventSerializer(serializers.ModelSerializer):
#     """Сериализатор событий"""

#     establishment = serializers.SlugRelatedField(
#         slug_field="name",
#         read_only=True,
#     )
#     image = Base64ImageField()

#     class Meta:
#         model = Event
#         fields = (
#             "name",
#             "establishment",
#             "description",
#             "date_start",
#             "date_end",
#             "type_event",
#             "price",
#             "image",
#         )


# class EventEditSerializer(serializers.ModelSerializer):
#     """Сериализатор событий"""

#     establishment = serializers.SlugRelatedField(
#         slug_field="name",
#         read_only=True,
#     )

#     class Meta:
#         model = Event
#         fields = (
#             "name",
#             "establishment",
#             "description",
#             "date_start",
#             "date_end",
#             "type_event",
#             "price",
#         )

#     def to_representation(self, instance):
#         return EventSerializer(
#             instance,
#             context={"request": self.context.get("request")},
#         ).data

#     def validate(self, data):
#         name = data.get("name")
#         date_start = data.get("date_start")
#         if Event.objects.filter(name=name, date_start=date_start).exists():
#             raise ValueError()

#     def create(self, validated_data):
#         type_event = validated_data.pop("type_event")
#         event = Event.objects.create(**validated_data)
#         event.kitchens.set(type_event)
#         return event

#     def update(self, instance, validated_data):
#         if "type_event" in validated_data:
#             instance.type_event.set(validated_data.pop("type_event"))

#         return super().update(
#             instance,
#             validated_data,
#         )

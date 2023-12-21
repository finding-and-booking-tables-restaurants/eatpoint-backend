from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from establishments.models import Establishment
from events.models import Event, TypeEvent, EventPhoto
from events.crud import list_event_types


class EventPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор полей объектов Фото события."""

    image = Base64ImageField()

    class Meta:
        model = EventPhoto
        fields = ("id", "image")


class TypeEventSerializer(serializers.ModelSerializer):
    """Сериализатор полей Типов событий."""

    class Meta:
        model = TypeEvent
        fields = ("id", "name")


class EstInEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ("id", "name", "address", "telephone")


class BaseEventSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Событий."""

    establishment = EstInEventSerializer(read_only=True)

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

    type_event = TypeEventSerializer(many=True)


class RetrieveEventSrializer(BaseEventSerializer):
    """Сериализатор Событий для 1 экземпляра."""

    type_event = TypeEventSerializer(many=True)
    photos = EventPhotoSerializer(many=True)

    class Meta(BaseEventSerializer.Meta):
        fields = BaseEventSerializer.Meta.fields + (
            "description",
            "date_end",
            "photos",
        )


class CreateEditEventSerializer(BaseEventSerializer):
    """Сериализатор полей для создания/изменения События."""

    image = Base64ImageField()

    class Meta(BaseEventSerializer.Meta):
        fields = BaseEventSerializer.Meta.fields + (
            "description",
            "date_end",
        )

    def to_representation(self, instance):
        return RetrieveEventSrializer(instance=instance)

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from establishments.models import Establishment
from events.models import Event, TypeEvent, EventPhoto, RecurSetting
from events.crud import event_exists, list_recurrencies


class RecurSettingSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор полей Настроек повтора события."""

    class Meta:
        model = RecurSetting
        fields = ("recurrence", "date_end")

    def to_representation(self, instance):
        return {
            "recurrence": instance.recurrence.description,
            "date_end": instance.date_end,
        }


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
    recur_settings = RecurSettingSerializer()

    class Meta(BaseEventSerializer.Meta):
        fields = BaseEventSerializer.Meta.fields + (
            "description",
            "photos",
            "recur_settings",
        )

    def get_recurrence(self, obj):
        if obj.recur_settings:
            return obj.recur_settings.recurrence.description
        return None

    def get_date_end(self, obj):
        if obj.recur_settings:
            return obj.recur_settings.date_end
        return None


class CreateEventSerializer(BaseEventSerializer):
    """Сериализатор полей для создания/изменения События."""

    recur_settings = RecurSettingSerializer(required=False)
    image = Base64ImageField()

    class Meta(BaseEventSerializer.Meta):
        fields = BaseEventSerializer.Meta.fields + (
            "description",
            "recur_settings",
            "photos",
        )

    def validate(self, attrs):
        name, date_start = attrs.get("name"), attrs.get("date_start")
        est_id = self.context.get("view").kwargs.get("establishment_id")
        if event_exists(
            establishment_id=est_id, name=name, date_start=date_start
        ):
            raise serializers.ValidationError("Событие уже создано")
        return attrs

    def to_representation(self, instance):
        return RetrieveEventSrializer(instance=instance).data


class UpdateEventSerializer(BaseEventSerializer):
    """Сериализатор полей для создания/изменения События."""

    image = Base64ImageField()

    class Meta(BaseEventSerializer.Meta):
        fields = BaseEventSerializer.Meta.fields + ("description",)

    def validate(self, attrs):
        name, date_start = attrs.get("name"), attrs.get("date_start")
        est_id = self.context.get("view").kwargs.get("establishment_id")
        if not self.instance and event_exists(
            establishment_id=est_id, name=name, date_start=date_start
        ):
            raise serializers.ValidationError("Событие уже создано")
        return attrs

    def to_representation(self, instance):
        return RetrieveEventSrializer(instance=instance).data

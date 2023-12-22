from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from api.permissions import IsEstOwner
from api.serializers import events as ser
from events import crud

from . import schema


@extend_schema(tags=["Типы событий"])
@extend_schema_view(**schema.events_types_schema)
class TypeEventViewset(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки Типов событий."""

    queryset = crud.list_event_types()
    serializer_class = ser.TypeEventSerializer


class BaseEventViewset(viewsets.ModelViewSet):
    """Базовый вьюсет для обработки Событий."""

    def _get_establishment_id(self) -> None:
        est_id = self.kwargs.get("establishment_id")
        if crud.establishment_exists(id=est_id):
            return est_id
        raise Http404("Заведение не найдено.")

    def get_queryset(self):
        return crud.list_events(establishment_id=self._get_establishment_id())


@extend_schema(tags=["События"])
@extend_schema_view(**schema.users_events_schema)
class EventUsersViewSet(BaseEventViewset):
    """Вьюсет для обработки Событий для пользователей."""

    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "list":
            return ser.ListEventSerializer
        return ser.RetrieveEventSrializer


@extend_schema(tags=["Бизнес (события)"])
@extend_schema_view(**schema.business_events_schema)
class EventBusinessViewSet(BaseEventViewset):
    """Вьюсет для обработки Событий для ресторатора."""

    permission_classes = (IsEstOwner,)
    http_method_names = ["get", "post", "delete", "patch"]

    def get_serializer_class(self):
        if self.action == "list":
            return ser.ListEventSerializer
        if self.action == "retrieve":
            return ser.RetrieveEventSrializer
        return ser.CreateEditEventSerializer

    def perform_create(self, serializer):
        est_id = self._get_establishment_id()
        crud.create_event(est_id=est_id, data=serializer.validated_data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_update(self, serializer):
        crud.update_event(
            event=serializer.instance, data=serializer.validated_data
        )


@extend_schema(tags=["Бизнес (события)"])
@extend_schema_view(**schema.events_photo_schema)
class EventPhotoViewset(viewsets.ModelViewSet):
    """Вьюсет для обработки Фото событий."""

    http_method_names = ["get", "post", "delete"]
    serializer_class = ser.EventPhotoSerializer
    permission_classes = (IsEstOwner,)

    def _get_event_id(self) -> None:
        event_id = self.kwargs.get("event_id")
        if crud.event_exists(id=event_id):
            return event_id
        return Http404("Событие не найдено.")

    def get_queryset(self):
        return crud.list_event_photos(event_id=self._get_event_id())

    def perform_create(self, serializer):
        return serializer.save(event_id=self._get_event_id())

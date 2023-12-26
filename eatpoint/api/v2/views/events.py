from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.permissions import IsEstOwner
from api.v2.schemas import events as schema
from api.v2.serializers import events as ser
from events import crud
from events.services import create_event


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
        return crud.list_future_events(
            establishment_id=self._get_establishment_id()
        )


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
# @extend_schema_view(**schema.business_events_schema)
class EventBusinessViewSet(BaseEventViewset):
    """Вьюсет для обработки Событий для ресторатора."""

    permission_classes = (IsEstOwner,)
    http_method_names = ["get", "post", "delete", "patch"]

    def get_serializer_class(self):
        if self.action == "list":
            return ser.ListEventSerializer
        if self.action == "retrieve":
            return ser.RetrieveEventSrializer
        if self.action == "create":
            return ser.CreateEventSerializer
        # TODO дописать сериализатор на изменение
        # return ser.CreateEditEventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        est_id = self._get_establishment_id()
        create_event(est_id=est_id, data=serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        crud.update_event(
            event=serializer.instance, data=serializer.validated_data
        )


@extend_schema(tags=["Бизнес (события)"])
@extend_schema_view(**schema.events_photo_schema)
class EventPhotoViewset(viewsets.ModelViewSet):
    """Вьюсет для обработки Фото событий."""

    http_method_names = ["post", "delete"]
    serializer_class = ser.EventPhotoSerializer
    permission_classes = (IsEstOwner,)

    def _get_establishment_id(self) -> None:
        est_id = self.kwargs.get("establishment_id")
        if crud.establishment_exists(id=est_id):
            return est_id
        raise Http404("Заведение не найдено.")

    def perform_create(self, serializer):
        return serializer.save(establishment_id=self._get_establishment_id())

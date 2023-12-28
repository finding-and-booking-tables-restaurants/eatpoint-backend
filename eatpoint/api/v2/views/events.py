from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsEstOwner
from api.v2.schemas import events as schema
from api.v2.serializers import events as ser
from core.exeptions import EventHasNoSeriaException, SuchEventExistsException
from core.pagination import LargeResultsSetPagination
from events import crud
from events.services import (
    create_event,
    update_event,
    update_event_seria,
    delete_seria,
)


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
    pagination_class = LargeResultsSetPagination

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
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.action == "list":
            return ser.ListEventSerializer
        if self.action == "retrieve":
            return ser.RetrieveEventSrializer
        if self.action == "partial_update":
            return ser.UpdateEventSerializer
        return ser.CreateEventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        est_id = self._get_establishment_id()
        try:
            event = create_event(est_id=est_id, data=serializer.validated_data)
        except SuchEventExistsException as e:
            return self._send_error(message=e.message)
        serializer = ser.RetrieveEventSrializer(
            instance=event, context={"view": self, "request": request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.get_serializer(
            event, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        try:
            event = update_event(event=event, data=serializer.validated_data)
        except SuchEventExistsException as e:
            return self._send_error(message=e.message)
        serializer = ser.RetrieveEventSrializer(
            instance=event, context={"view": self, "request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def update_seria(self, request, establishment_id: int, pk: int):
        event = self.get_object()
        serializer = self.get_serializer(
            event, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        try:
            event = update_event_seria(event, serializer.validated_data)
        except (SuchEventExistsException, EventHasNoSeriaException) as e:
            return self._send_error(message=e.message)
        serializer = ser.RetrieveEventSrializer(
            instance=event, context={"view": self, "request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["delete"], detail=True)
    def delete_seria(self, request, establishment_id: int, pk: int):
        event = self.get_object()
        try:
            deleted = delete_seria(event=event)
        except EventHasNoSeriaException as e:
            return self._send_error(message=e.message)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def _send_error(self, message):
        error = {"non_field_errors": [message]}
        return Response(data=error, status=status.HTTP_400_BAD_REQUEST)


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


@extend_schema(tags=["Периоды повтора событий"])
@extend_schema_view(**schema.recurrencies_schema)
class ReccurenceViewset(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки вариантов повторения событий."""

    queryset = crud.list_recurrencies()
    serializer_class = ser.RecurrenceSerializer

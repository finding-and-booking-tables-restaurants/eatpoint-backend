from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from api.permissions import IsRestorateurEdit
from api.serializers import events as ser
from events import crud

from . import schema


@extend_schema(tags=["События"])
class TypeEventViewset(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки Типов событий."""

    queryset = crud.list_event_types()
    serializer_class = ser.TypeEventSerializer


class BaseEventViewset(viewsets.ModelViewSet):
    """Базовый вьюсет для обработки Событий."""

    def _get_establishment_id(self) -> None:
        est_id = self.kwargs.get("establishment_id")
        if crud.establishment_exists(est_id=est_id):
            return est_id
        return Http404("Заведение не найдено.")

    def get_queryset(self):
        return crud.list_events(establishment_id=self._get_establishment_id())


@extend_schema(tags=["События"])
@extend_schema_view(**schema.business_events_schema)
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

    permission_classes = (IsRestorateurEdit,)
    http_method_names = ["get", "post", "delete", "patch"]

    def get_serializer_class(self):
        if self.action == "list":
            return ser.ListEventSerializer
        if self.action == "retrieve":
            return ser.RetrieveEventSrializer
        return ser.CreateEditEventSerializer

    def perform_create(self, serializer):
        est_id = self._get_establishment_id()
        crud.add_event(est_id=est_id, data=serializer.validated_data)

    def perform_update(self, serializer):
        crud.edit_event(
            event=serializer.instance, data=serializer.validated_data
        )


# @extend_schema(
#     tags=["События"],
#     methods=["GET", "POST", "PATCH", "DELETE"],
# )
# @extend_schema_view(
#     list=extend_schema(
#         summary="Получить список событий к заведению с id=",
#         description="Клиент/ресторатор",
#     ),
# )
# class EventUsersViewSet(viewsets.ModelViewSet):
#     """Вьюсет: Отзывы(пользователь)"""

#     serializer_class = EventSerializer
#     http_method_names = ["get"]

#     def get_queryset(self):
#         establishment_id = self.kwargs.get("establishment_id")
#         establishment = get_object_or_404(Establishment, id=establishment_id)
#         return establishment.event.all()

#     def perform_create(self, serializer):
#         establishment_id = self.kwargs.get("establishment_id")
#         establishment = get_object_or_404(Establishment, id=establishment_id)
#         serializer.save(establishment=establishment)


# class EventBusinessViewSet(viewsets.ModelViewSet):
#     """Вьюсет события(бизнес)"""

#     serializer_class = EventSerializer
#     http_method_names = ["get", "post", "patch", "delete"]
#     permission_classes = (IsRestorateurEdit,)

#     # def get_serializer_class(self):
#     #     if self.request.method in SAFE_METHODS:
#     #         return EventSerializer
#     #     return EventEditSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Event.objects.filter(establishment__owner=user)

#     def perform_create(self, serializer):
#         establishment_id = self.kwargs.get("establishment_id")
#         establishment = get_object_or_404(Establishment, id=establishment_id)
#         serializer.save(establishment=establishment)

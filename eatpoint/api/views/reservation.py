from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS

from core.pagination import LargeResultsSetPagination
from establishments.models import Establishment, ZoneEstablishment
from api.serializers.reservations import (
    ReservationsEditSerializer,
    AuthReservationsEditSerializer,
)


@extend_schema(
    tags=["Бронирование"], methods=["GET", "POST", "PATCH", "PUT", "DELETE"]
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список броней заведения",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о броне заведения",
    ),
    create=extend_schema(
        summary="Добавить бронирование",
        description="Для авторизованного пользователя имя, фамилия, телефон, почта заполняются автоматически",
    ),
    partial_update=extend_schema(
        summary="Изменить данные бронирования",
    ),
    destroy=extend_schema(
        summary="Удалить бронирование",
    ),
)
class ReservationsViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования 1"""

    http_method_names = ["get", "post", "patch", "options"]
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if (
            self.request.user.is_anonymous
            or self.request.method in SAFE_METHODS
        ):
            return ReservationsEditSerializer
        return AuthReservationsEditSerializer

    def get_queryset(self):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        return establishment.reservation.all()

    def perform_create(self, serializer):
        zone = serializer.validated_data.get("zone")
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        if not ZoneEstablishment.objects.filter(
            establishment=establishment, zone=zone
        ):
            raise ValidationError(
                "Выбранная зона не принадлежит к указанному заведению."
            )
        user = self.request.user
        if self.request.user.is_anonymous:
            serializer.save(user=None, establishment=establishment)
        else:
            serializer.save(
                user=user,
                establishment=establishment,
                telephone=user.telephone,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )

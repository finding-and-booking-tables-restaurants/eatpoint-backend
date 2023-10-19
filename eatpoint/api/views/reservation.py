from drf_spectacular.utils import extend_schema, extend_schema_view
from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework import viewsets, status

from api.permissions import IsUserReservation
from core.pagination import LargeResultsSetPagination
from core.validators import validate_reservation_time_zone
from establishments.models import Establishment
from api.serializers.reservations import (
    ReservationsEditSerializer,
    AuthReservationsEditSerializer,
    ReservationsHistoryEditSerializer,
)
from reservation.models import Reservation, ReservationHistory


@extend_schema(
    tags=["Бронирование"],
    methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    description="Клиент",
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
    ),
    partial_update=extend_schema(
        summary="Изменить данные бронирования",
    ),
    destroy=extend_schema(
        summary="Удалить бронирование",
    ),
)
class ReservationsViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования"""

    http_method_names = ["post", "patch"]
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsUserReservation,)

    def get_serializer_class(self):
        """Выбор serializer_class в зависимости от типа запроса"""
        if (
            self.request.user.is_anonymous
            or self.request.method in SAFE_METHODS
        ):
            return ReservationsEditSerializer
        return AuthReservationsEditSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Response(
                {"errors": "Вы не авторизованы"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        establishment = self.kwargs.get("establishment_id")
        reservation = Reservation.objects.filter(
            user=user, establishment=establishment
        )
        return reservation

    def perform_create(self, serializer):
        data = serializer.validated_data
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        validate_reservation_time_zone(data, establishment)
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


@extend_schema(
    tags=["Мои бронирования"],
    methods=["GET", "DELETE"],
    description="Клиент/ресторатор",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список бронирований",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о бронировании заведения",
    ),
    destroy=extend_schema(
        summary="Удалить бронирование",
    ),
)
class ReservationsListViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования"""

    http_method_names = ["get", "delete"]
    pagination_class = LargeResultsSetPagination
    serializer_class = AuthReservationsEditSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_user:
            reservation = Reservation.objects.filter(user=user)
            return reservation
        elif user.is_restorateur:
            reservation_rest = Reservation.objects.filter(
                establishment__owner=user
            )
            return reservation_rest
        return Response(
            {"errors": "Вы не авторизованы"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        reservation_id = self.kwargs.get("pk")
        removable = Reservation.objects.filter(user=user, id=reservation_id)
        if not removable.exists():
            return Response(
                {"errors": "Бронирование отсутствует"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        removable.delete()
        return Response(
            {"message": "Бронирование удалено"},
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(
    tags=["История бронирования"],
    methods=["GET"],
    description="Клиент/ресторатор",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список истории броней заведения",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о броне заведения",
    ),
)
class ReservationsHistoryListViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования"""

    http_method_names = ["get"]
    pagination_class = LargeResultsSetPagination
    serializer_class = ReservationsHistoryEditSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_user:
            reservation = ReservationHistory.objects.filter(user=user)
            return reservation
        elif user.is_restorateur:
            reservation_rest = ReservationHistory.objects.filter(
                establishment__owner=user
            )
            return reservation_rest
        return Response(
            {"errors": "Вы не авторизованы"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

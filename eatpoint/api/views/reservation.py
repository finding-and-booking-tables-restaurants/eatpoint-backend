from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import OpenApiParameter
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status

from api.permissions import IsUserReservationCreate, IsRestorateur, IsClient
from core.pagination import LargeResultsSetPagination
from core.validators import (
    validate_reserv_anonim,
)
from establishments.models import Establishment
from api.serializers.reservations import (
    ReservationsEditSerializer,
    # AuthReservationsEditSerializer,
    ReservationsHistoryEditSerializer,
    ReservationsUserListSerializer,
    ReservationsRestorateurListSerializer,
    AvailabilitySerializer,
)
from reservation.models import (
    Reservation,
    ReservationHistory,
    ConfirmationCode,
    Availability,
)


@extend_schema(
    tags=["Бронирование"],
    methods=["POST"],
    description="Клиент",
)
@extend_schema_view(
    create=extend_schema(
        summary="Добавить бронирование",
        parameters=[
            OpenApiParameter(
                name="establishment_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
)
class ReservationsEditViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования"""

    http_method_names = ["post"]
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsUserReservationCreate,)
    serializer_class = ReservationsEditSerializer

    # def get_serializer_class(self):
    #     """Выбор serializer_class в зависимости от типа запроса"""
    #     if (
    #         self.request.user.is_anonymous
    #         or self.request.method in SAFE_METHODS
    #     ):
    #         return ReservationsEditSerializer
    #     return AuthReservationsEditSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            establishment = self.kwargs.get("establishment_id")
            reservation = Reservation.objects.filter(
                user=user, establishment=establishment
            )
            return reservation

    def create(self, request, *args, **kwargs):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        user = self.request.user
        telephone = request.data.get("telephone")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.is_anonymous:
            validate_reserv_anonim(user, request.data)

            try:
                ConfirmationCode.objects.get(
                    phone_number=telephone, is_verified=True
                )
            except ConfirmationCode.DoesNotExist:
                return Response(
                    {"detail": "Подтвердите номер телефона!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(user=None, establishment=establishment)
            return Response(serializer.data)
        else:
            serializer.save(
                user=user,
                establishment=establishment,
                telephone=user.telephone,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )

            return Response(serializer.data)


@extend_schema(
    tags=["Мои бронирования"],
    methods=["GET", "DELETE", "PATCH"],
    description="Клиент/ресторатор",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список бронирований",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о бронировании заведения",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
    destroy=extend_schema(
        summary="Удалить бронирование",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
    partial_update=extend_schema(
        summary="Изменить данные бронирования",
        parameters=[
            OpenApiParameter(
                name="establishment_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            ),
        ],
    ),
)
class ReservationsUserListViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования"""

    http_method_names = ["get", "patch", "delete"]
    pagination_class = LargeResultsSetPagination
    permission_classes = [
        IsClient,
    ]
    serializer_class = ReservationsUserListSerializer

    def get_queryset(self):
        user = self.request.user
        reservation = Reservation.objects.filter(user=user)
        return reservation

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
            status=status.HTTP_404_NOT_FOUND,
        )


@extend_schema(
    tags=["Бизнес(бронирования)"],
    methods=["GET", "DELETE"],
    description="Ресторатор",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список бронирований",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о бронировании заведения",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
    destroy=extend_schema(
        summary="Удалить бронирование",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
)
class ReservationsRestorateurListViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования"""

    http_method_names = ["get", "delete"]
    pagination_class = LargeResultsSetPagination
    permission_classes = [
        IsRestorateur,
    ]
    serializer_class = ReservationsRestorateurListSerializer

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(establishment__owner=user)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        reservation_id = self.kwargs.get("pk")
        removable = Reservation.objects.filter(
            establishment__owner=user,
            id=reservation_id,
        )
        if not removable.exists():
            return Response(
                {"errors": "Бронирование отсутствует"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        removable.delete()
        return Response(
            {"message": "Бронирование удалено"},
            status=status.HTTP_404_NOT_FOUND,
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
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
)
class ReservationsHistoryListViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования"""

    http_method_names = ["get"]
    pagination_class = LargeResultsSetPagination
    serializer_class = ReservationsHistoryEditSerializer
    permission_classes = [
        IsRestorateur | IsClient,
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_client:
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


@extend_schema(
    tags=["Слоты для бронирования"],
    methods=["GET"],
    description="Все пользователи",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список слотов к заведению с id",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о слоте",
    ),
)
class AvailabilityViewSet(viewsets.ModelViewSet):
    """Вьюсет: Слоты"""

    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    http_method_names = ["get"]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        establishment_id = self.kwargs.get("establishment_id")
        return Availability.objects.filter(establishment=establishment_id)

from datetime import datetime

from django.conf import settings as django_settings
from django.core.mail import send_mail
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins

from api.permissions import (
    IsUserReservationCreate,
    IsRestorateur,
    IsClient,
    IsRestorateurEdit,
)
from api.v2.views.schema import (
    reservations_edit_schema,
    reservations_edit_schema_view,
    ReservationsUserListViewSet_schema,
    ReservationsUserListViewSet_schema_view,
    ReservationsRestorateurListViewSet_schema,
    ReservationsRestorateurListViewSet_schema_view,
    ReservationsHistoryListViewSet_schema,
    ReservationsHistoryListViewSet_schema_view,
)
from core.pagination import LargeResultsSetPagination
from core.validators import (
    validate_reserv_anonim,
)
from establishments.models import Establishment
from api.v2.serializers.reservations import (
    ReservationsEditSerializer,
    ReservationsHistoryEditSerializer,
    ReservationsUserListSerializer,
    ReservationsRestorateurListSerializer,
    UpdateReservationStatusSerializer,
    AvailableSlotsSerializer,
    UpdateReservationVisitedSerializer,
)
from reservation.models import (
    Reservation,
    ReservationHistory,
    ConfirmationCode,
    Slot,
)


@extend_schema(**reservations_edit_schema)
@extend_schema_view(**reservations_edit_schema_view)
class ReservationsEditViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для создания бронирования для не авторизованного пользователя"""

    http_method_names = ["post"]
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsUserReservationCreate,)
    serializer_class = ReservationsEditSerializer
    queryset = Reservation.objects.all()

    def create(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        slots_ids = list(self.request.data.get("slots", []))
        user = self.request.user

        if user.is_anonymous:
            validate_reserv_anonim(user, self.request.data)
            telephone = self.request.data.get("telephone")
            email = self.request.data.get("email")
            first_name = self.request.data.get("first_name")
            last_name = self.request.data.get("last_name")

            try:
                ConfirmationCode.objects.get(email=email, is_verified=True)
            except ConfirmationCode.DoesNotExist:
                return Response(
                    {"detail": "Подтвердите номер телефона!"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            reservation = Reservation.objects.create(
                user=None,
                telephone=telephone,
                email=email,
                first_name=first_name,
                last_name=last_name,
                establishment=establishment,
                comment=self.request.data.get("comment"),
            )
        else:
            reservation = Reservation.objects.create(
                user=user,
                telephone=user.telephone,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                establishment=establishment,
                comment=self.request.data.get("comment"),
            )

        try:
            slots = Slot.objects.filter(
                establishment=establishment_id, id__in=slots_ids
            )
            reservation.slots.set(slots)
            reservation.date_reservation = slots[0].date
            reservation.start_time_reservation = slots[0].time
            reservation.save()
            slots.update(is_active=False)

        except IndexError:
            return Response(
                {"detail": "Слотов с данными id нет!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = f"""
            Подтвердите бронирование:
            заведение: {establishment.name},\n
            зона: {slots[0].zone},\n
            дата: {slots[0].date} {slots[0].time},\n
            стол No{slots[0].table.number},\n
            мест: {slots[0].table.seats},\n
            для пользователя:\n
            {reservation.first_name} {reservation.last_name},\n
            {reservation.email},\n
            {reservation.telephone}\n
        """

        send_mail(
            "Подтвердите бронирование",
            message=message,
            from_email=django_settings.EMAIL_HOST_USER,
            recipient_list=[reservation.establishment.owner.email],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(**ReservationsUserListViewSet_schema)
@extend_schema_view(**ReservationsUserListViewSet_schema_view)
class ReservationsUserListViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования для клиента"""

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
            status=status.HTTP_200_OK,
        )


@extend_schema(**ReservationsRestorateurListViewSet_schema)
@extend_schema_view(**ReservationsRestorateurListViewSet_schema_view)
class ReservationsRestorateurListViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки бронирования для ресторатора"""

    http_method_names = ["get", "delete", "patch"]
    pagination_class = LargeResultsSetPagination
    permission_classes = [
        IsRestorateurEdit,
    ]

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(
            establishment__owner=user,
        )

    def get_serializer_class(self):
        """Выбор serializer_class в зависимости от типа запроса"""
        if self.request.method == "PATCH" and self.request.data.get(
            "is_accepted"
        ):
            return UpdateReservationStatusSerializer
        elif self.request.method == "PATCH" and self.request.data.get(
            "is_visited"
        ):
            return UpdateReservationVisitedSerializer
        return ReservationsRestorateurListSerializer

    def destroy(self, request, *args, **kwargs):
        """Удаление бронирования"""
        user = self.request.user
        current_datetime = datetime.now()
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
        new_removable = Reservation.objects.filter(
            establishment__owner=user,
            id=reservation_id,
            is_accepted=True,
            date_reservation__gte=current_datetime,
        )
        if new_removable.exists():
            return Response(
                {"errors": "Нельзя удалить подтвержденное бронирование."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        removable.delete()
        return Response(
            {"message": "Бронирование удалено"},
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        """Изменяет статус бронирования и статус посещения"""
        instance = self.get_object()
        date_reservation = datetime.combine(
            instance.date_reservation,
            datetime.strptime(instance.start_time_reservation, "%H:%M").time(),
        )

        if instance.is_accepted and request.data.get("is_accepted"):
            return Response(
                {"error": "Бронирование уже подтверждено"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if instance.is_visited and request.data.get("is_visited"):
            return Response(
                {"error": "Заведение уже посещено"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not instance.is_accepted and request.data.get("is_visited"):
            return Response(
                {"error": "Бронирование еще не подтверждено"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
            request.data.get("is_visited")
            and date_reservation > datetime.now()
        ):
            return Response(
                {"error": "Время бронирования еще не наступило"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer_class()
        serializer = serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email = instance.email
        message = f"""
            Бронирование подтверждено!\n
            {instance},\n
            адрес: {instance.establishment.cities} \
            {instance.establishment.address}
            """

        send_mail(
            "Бронирование подтверждено!",
            message,
            django_settings.EMAIL_HOST_USER,
            [email],
        )
        return Response(
            {"complete": "Бронирование подтверждено!"},
            status=status.HTTP_200_OK,
        )


@extend_schema(**ReservationsHistoryListViewSet_schema)
@extend_schema_view(**ReservationsHistoryListViewSet_schema_view)
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
class AvailableSlotsViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Список свободных слотов"""

    serializer_class = AvailableSlotsSerializer
    http_method_names = ["get"]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        establishment_id = self.kwargs.get("establishment_id")
        current_date = datetime.today().date()
        current_time = datetime.now().time().strftime("%H:%M")
        slots = (
            Slot.objects.filter(establishment=establishment_id)
            .filter(is_active=True)
            .filter(
                Q(date=current_date, time__gte=current_time)
                | Q(date__gt=current_date)
            )
            .order_by("date", "time", "zone")
        )

        return slots

    def retrieve(self, request, *args, **kwargs):
        try:
            slot = self.get_object()
            serializer = self.get_serializer(slot)
            return Response(serializer.data)
        except Slot.DoesNotExist:
            return Response(
                {
                    "errors": f"слота с id {self.kwargs.get('pk')} "
                    f"не существует или он занят"
                },
            )


class AvailabilityViewSet(viewsets.ModelViewSet):
    """Вьюсет: Слоты"""


#
#     queryset = Availability.objects.all()
#     serializer_class = AvailabilitySerializer
#     http_method_names = ["get"]
#     pagination_class = LargeResultsSetPagination
#
#     def get_queryset(self):
#         establishment_id = self.kwargs.get("establishment_id")
#         return Availability.objects.filter(establishment=establishment_id)

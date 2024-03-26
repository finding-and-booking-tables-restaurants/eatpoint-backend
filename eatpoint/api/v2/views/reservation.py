from datetime import datetime

from django.conf import settings as django_settings
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins

from api.v2.filters.reservations import SlotsFilter
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
    AvailableSlotsViewSet_schema,
    AvailableSlotsViewSet_schema_view,
)
from core.pagination import LargeResultsSetPagination, SlotsPagination
from core.validators import (
    validate_reserv_anonim,
)
from establishments.models import Establishment
from api.v2.serializers.reservations import (
    ReservationsUnregUserSerializer,
    ReservationsHistoryEditSerializer,
    ReservationsUserListSerializer,
    ReservationsRestorateurListSerializer,
    AvailableSlotsSerializer,
    ReservationsUserSerializer,
    UpdateReservationActionSerializer,
)
from reservation.models import (
    Reservation,
    ReservationHistory,
    ConfirmationCode,
    Slot,
)


@extend_schema(tags=["Бронирование"], **reservations_edit_schema)
@extend_schema_view(**reservations_edit_schema_view)
class ReservationsEditViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для создания бронирования"""

    http_method_names = [
        "post",
    ]
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsUserReservationCreate,)
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_anonymous:
            return ReservationsUnregUserSerializer
        else:
            return ReservationsUserSerializer

    def create(self, request, *args, **kwargs):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        slots_ids = list(request.data.get("slots", []))
        user = request.user

        if user.is_anonymous:
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            validate_reserv_anonim(user, request.data)
            email = request.data.get("email")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            telephone = request.data.get("telephone")

            try:
                unregistered_user = ConfirmationCode.objects.get(
                    email=email, is_verified=True
                )
            except unregistered_user.DoesNotExist:
                return Response(
                    {"detail": "email не подтвержден!"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            reservation = serializer.save(
                user=None, establishment=establishment
            )

        else:
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            first_name = user.first_name
            last_name = user.last_name
            email = user.email
            telephone = user.telephone

            reservation = serializer.save(
                user=user,
                establishment=establishment,
                first_name=first_name,
                last_name=last_name,
                email=email,
                telephone=telephone,
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
            заведение: {establishment.name},
            зона: {slots[0].zone},
            дата: {slots[0].date} {slots[0].time},
            стол No{slots[0].table.number},
            мест: {slots[0].table.seats},
            для пользователя:
            {first_name} {last_name},
            {email},
            {telephone}
        """

        send_mail(
            "Подтвердите бронирование",
            message=message,
            from_email=django_settings.EMAIL_HOST_USER,
            recipient_list=[reservation.establishment.owner.email],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Мои бронирования"], **ReservationsUserListViewSet_schema)
@extend_schema_view(**ReservationsUserListViewSet_schema_view)
class ReservationsUserListViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для обработки бронирования для клиента"""

    http_method_names = ["get", "patch", "delete"]
    pagination_class = LargeResultsSetPagination
    permission_classes = [
        IsClient,
    ]
    serializer_class = ReservationsUserListSerializer

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(user=user).select_related(
            "establishment", "slots", "zone", "table"
        )

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        try:
            removable = self.get_object()
        except Http404:
            return Response(
                {"errors": "Бронирование отсутствует"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        date_reservation = removable.date_reservation
        time_reservation = datetime.strptime(
            removable.start_time_reservation, "%H:%M"
        ).time()
        reservation_date_time = datetime.combine(
            date_reservation, time_reservation
        )

        # бронь не подтверждена, время не наступило, не клиент
        if (
            not removable.is_accepted
            and not removable.is_visited
            and not user.is_client
            and datetime.now() < reservation_date_time
        ):
            return Response(
                {
                    "errors": """если Бронь не подтверждена,
                 время не наступило, может удалить только клиент"""
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # бронь подтверждена, время не наступило,
        #  не клиент или не ресторатор
        if (
            removable.is_accepted
            and not removable.is_visited
            and datetime.now() < reservation_date_time
            and (not user.is_client or not user.is_restorateur)
        ):
            return Response(
                {
                    "errors": """если Бронь подтверждена, время не наступило,
                 может удалить только клиент или ресторатор"""
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # бронь подтверждена, время наступило, не выполнено
        if (
            removable.is_accepted
            and reservation_date_time < datetime.now()
            and not removable.is_visited
        ):
            return Response(
                {
                    "errors": """если Бронь подтверждена, время наступило
                 и не выполнена, удалить бронь нельзя"""
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # бронь подтверждена, время наступило, выполнено
        if (
            removable.is_accepted
            and reservation_date_time < datetime.now()
            and removable.is_visited
        ):
            return Response(
                {"errors": "если Бронь выполнена, удалить бронь нельзя"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # восстановление активности слотов перед удалением брони
        if (
            not removable.is_accepted
            and datetime.now() < reservation_date_time
        ):
            slot_ids = removable.slots.values_list("id", flat=True)
            for slot_id in slot_ids:
                Slot.objects.filter(id=slot_id).update(is_active=True)

        removable.delete()

        return Response(
            {"message": "Бронирование удалено"},
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        """Изменяет статус бронирования и статус посещения"""
        instance = self.get_object()
        email = instance.email or instance.user.email
        reservation_date_time = datetime.combine(
            instance.date_reservation,
            datetime.strptime(instance.start_time_reservation, "%H:%M").time(),
        )

        action = request.data.get("action")

        match action:
            case "is_deleted":
                if instance.is_deleted:
                    return Response(
                        {"error": "Бронирование уже отменено"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if instance.is_visited:
                    return Response(
                        {"error": "Нельзя отменить бронь, если посещено"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if (
                    instance.is_accepted
                    and datetime.now() < reservation_date_time
                ):
                    slot_ids = instance.slots.values_list("id", flat=True)
                    for slot_id in slot_ids:
                        Slot.objects.filter(id=slot_id).update(is_active=True)
                subj = "Бронирование отменено!"
                instance.is_deleted = True

            case _:
                return Response(
                    {"error": f"метод {action} не поддерживается"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.get_serializer_class()
        serializer = serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message = f"""
            {subj}
            {instance},
            адрес: {instance.establishment.cities}
            {instance.establishment.address}
            """

        send_mail(
            subj,
            message,
            django_settings.EMAIL_HOST_USER,
            [email],
        )

        return Response(
            {"complete": subj},
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Бизнес(бронирования)"], **ReservationsRestorateurListViewSet_schema
)
@extend_schema_view(**ReservationsRestorateurListViewSet_schema_view)
class ReservationsRestorateurListViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для обработки бронирования для ресторатора"""

    http_method_names = ["get", "delete", "patch"]
    pagination_class = LargeResultsSetPagination
    permission_classes = [
        IsRestorateurEdit,
    ]

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(
            establishment__email=user.email,
        ).order_by("date_reservation", "start_time_reservation")

    def get_serializer_class(self):
        """Выбор serializer_class в зависимости от типа запроса"""
        if self.request.method == "PATCH" and self.request.data.get("action"):
            return UpdateReservationActionSerializer
        return ReservationsRestorateurListSerializer

    def destroy(self, request, *args, **kwargs):
        """Удаление бронирования"""
        user = request.user
        try:
            removable = self.get_object()
        except Http404:
            return Response(
                {"errors": "Бронирование отсутствует"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        date_reservation = removable.date_reservation
        time_reservation = datetime.strptime(
            removable.start_time_reservation, "%H:%M"
        ).time()
        reservation_date_time = datetime.combine(
            date_reservation, time_reservation
        )

        # бронь не подтверждена, время не наступило, не клиент
        if (
            not removable.is_accepted
            and not removable.is_visited
            and not user.is_client
            and datetime.now() < reservation_date_time
        ):
            return Response(
                {
                    "errors": """если Бронь не подтверждена,
                 время не наступило, может удалить только клиент"""
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # бронь подтверждена, время не наступило,
        #  не клиент или не ресторатор
        if (
            removable.is_accepted
            and not removable.is_visited
            and datetime.now() < reservation_date_time
            and (not user.is_client or not user.is_restorateur)
        ):
            return Response(
                {
                    "errors": """если Бронь подтверждена, время не наступило,
                 может удалить только клиент или ресторатор"""
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # бронь подтверждена, время наступило, не выполнено
        if (
            removable.is_accepted
            and reservation_date_time < datetime.now()
            and not removable.is_visited
            and removable.establishment.email != user.email
        ):
            return Response(
                {
                    "errors": """если Бронь подтверждена, время наступило
                 и не выполнена, удалить бронь может
                 только администратор заведения"""
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # бронь подтверждена, время наступило, выполнено
        if (
            removable.is_accepted
            and reservation_date_time < datetime.now()
            and removable.is_visited
        ):
            return Response(
                {"errors": "если Бронь выполнена, удалить бронь нельзя"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # восстановление слотов перед удалением брони если время не наступило
        if (
            not removable.is_accepted
            and datetime.now() < reservation_date_time
        ):
            slot_ids = removable.slots.values_list("id", flat=True)
            for slot_id in slot_ids:
                Slot.objects.filter(id=slot_id).update(is_active=True)

        removable.delete()

        return Response(
            {"message": "Бронирование удалено"},
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        """Изменяет статус бронирования и статус посещения"""
        instance = self.get_object()
        email = instance.email or instance.user.email
        reservation_date_time = datetime.combine(
            instance.date_reservation,
            datetime.strptime(instance.start_time_reservation, "%H:%M").time(),
        )

        subj = ""
        action = request.data.get("action")

        match action:
            case "is_accepted":
                if instance.is_accepted:
                    return Response(
                        {"error": "Бронирование уже подтверждено"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                subj = "Бронирование подтверждено!"
                instance.is_accepted = True

            case "is_visited":
                if instance.is_visited:
                    return Response(
                        {"error": "Заведение уже посещено"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if not instance.is_accepted:
                    return Response(
                        {"error": "Бронирование еще не подтверждено"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if reservation_date_time > datetime.now():
                    return Response(
                        {"error": "Время бронирования еще не наступило"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                subj = "Бронирование выполнено!"
                instance.is_visited = True

            case "is_deleted":
                if instance.is_deleted:
                    return Response(
                        {"error": "Бронирование уже отменено"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if instance.is_visited:
                    return Response(
                        {"error": "Нельзя отменить бронь, если посещено"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if (
                    instance.is_accepted
                    and datetime.now() < reservation_date_time
                ):
                    slot_ids = instance.slots.values_list("id", flat=True)
                    for slot_id in slot_ids:
                        Slot.objects.filter(id=slot_id).update(is_active=True)

                subj = "Бронирование отменено!"
                instance.is_deleted = True

        serializer = self.get_serializer_class()
        serializer = serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message = f"""
            {subj}
            {instance},
            адрес: {instance.establishment.cities}
            {instance.establishment.address}
            """

        send_mail(
            subj,
            message,
            django_settings.EMAIL_HOST_USER,
            [email],
        )

        return Response(
            {"complete": subj},
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["История бронирования"], **ReservationsHistoryListViewSet_schema
)
@extend_schema_view(**ReservationsHistoryListViewSet_schema_view)
class ReservationsHistoryListViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки истории бронирования"""

    http_method_names = ["get"]
    pagination_class = LargeResultsSetPagination
    serializer_class = ReservationsHistoryEditSerializer
    permission_classes = [
        IsRestorateur | IsClient,
    ]

    def get_queryset(self):
        user = self.request.user

        if user.is_client:
            return ReservationHistory.objects.filter(email=user.email)
        elif user.is_restorateur:
            return ReservationHistory.objects.filter(
                establishment__email=user.email
            )


@extend_schema(tags=["Слоты для бронирования"], **AvailableSlotsViewSet_schema)
@extend_schema_view(**AvailableSlotsViewSet_schema_view)
class AvailableSlotsViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Список свободных слотов"""

    serializer_class = AvailableSlotsSerializer
    http_method_names = ["get"]
    pagination_class = SlotsPagination
    filterset_class = SlotsFilter

    def get_queryset(self):
        establishment_id = self.kwargs.get("establishment_id")
        current_date = datetime.today().date()
        current_time = datetime.now().strftime("%H:%M")

        return (
            Slot.objects.all()
            .values(
                "id",
                "date",
                "time",
                "zone__zone",
                "table__number",
                "table__seats",
                "establishment__id",
                "establishment__name",
            )
            .filter(is_active=True)
            .filter(establishment__id=establishment_id)
            .filter(
                Q(date=current_date, time__gte=current_time)
                | Q(date__gt=current_date)
            )
            .order_by("id")
        )

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
    """Вьюсет: Слоты -----ЭТО ДЛЯ V1 ---------"""


#
#     queryset = Availability.objects.all()
#     serializer_class = AvailabilitySerializer
#     http_method_names = ["get"]
#     pagination_class = LargeResultsSetPagination
#
#     def get_queryset(self):
#         establishment_id = self.kwargs.get("establishment_id")
#         return Availability.objects.filter(establishment=establishment_id)

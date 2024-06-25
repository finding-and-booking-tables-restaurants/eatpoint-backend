from datetime import datetime

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import ExtractWeek, ExtractMonth
from django.db.models import Q


from api.permissions import IsRestorateur
from api.v2.serializers.analytics import (
    AnalyticsStaticSerializer,
    AnalyticsDynamicSerializer,
)
from establishments.models import Establishment
from reservation.models import Reservation, ReservationHistory
from rest_framework.response import Response


@extend_schema(
    tags=["Бизнес(аналитика заведения)"],
    description="Ресторатор",
    methods=["GET", "POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Получить историю бронирования за выбранное время",
    ),
    get=extend_schema(
        summary="Получить историю бронирования за день, неделю и год",
    ),
)
class AnalyticsHistoryViewSet(APIView):
    """
    Аналитика для 1 заведения.

    API endpoint для получения аналитики по бронированиям для определенного заведения.
    Предоставляет информацию о количестве бронирований по дням, неделям, месяцам и годам.

    Разрешения:
        - Только аутентифицированным пользователям (IsAuthenticated).
        - Пользователям, являющимся владельцами заведения (IsRestorateur).

    HTTP-методы:
        - GET: Получение статистики по бронированиям для определенного заведения.

    Параметры:
        - establishment_id: Идентификатор заведения для получения аналитики.

    """

    permission_classes = (IsAuthenticated, IsRestorateur)

    @extend_schema(
        responses=AnalyticsStaticSerializer,
    )
    def get(self, request, establishment_id):
        """
        Получение аналитики по бронированиям для определенного заведения.

        :param request: Объект запроса REST API.
        :param establishment_id: Идентификатор заведения для получения аналитики.
        :return: Данные аналитики по бронированиям для заведения или сообщение об ошибке.
        """
        establishment = Establishment.objects.get(pk=establishment_id)
        if request.user != establishment.owner:
            raise PermissionDenied(
                "Вы не являетесь владельцем этого заведения"
            )

        now_date = datetime.now().date()

        total_reservation = ReservationHistory.objects.filter(
            establishment=establishment_id
        ).count()

        daily_reservation = ReservationHistory.objects.filter(
            establishment=establishment_id,
            reservation_date__year=now_date.year,
            reservation_date__month=now_date.month,
            reservation_date__day=now_date.day,
        ).count()

        weekly_reservation = ReservationHistory.objects.filter(
            establishment=establishment_id,
            reservation_date__week=ExtractWeek(now_date),
        ).count()

        monthly_reservation = (
            ReservationHistory.objects.filter(
                establishment=establishment_id,
                reservation_date__year=now_date.year,
            )
            .annotate(month=ExtractMonth("reservation_date"))
            .values("month")
            .annotate(monthly_count=Count("id"))
        )

        yearly_reservation = (
            ReservationHistory.objects.filter(
                establishment=establishment_id,
                reservation_date__year=now_date.year,
            )
            .values(
                "reservation_date__year",
            )
            .annotate(yearly_count=Count("id"))
        )

        daily_reservations_by_day = (
            ReservationHistory.objects.filter(
                establishment=establishment_id,
            )
            .values("reservation_date__date")
            .annotate(reservation_count=Count("id"))
        )

        aggregated_data = {
            "total_reservation": total_reservation,
            "daily_reservation": daily_reservation,
            "weekly_reservation": weekly_reservation,
            "monthly_reservation": list(monthly_reservation),
            "yearly_reservation": yearly_reservation,
            "daily_reservations_by_day": list(daily_reservations_by_day),
        }

        serializer = AnalyticsStaticSerializer(aggregated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses=AnalyticsDynamicSerializer,
        request=AnalyticsDynamicSerializer,
    )
    def post(self, request, establishment_id):
        """
        Получение динамической аналитики по POST запросу.

        :param request: Объект запроса REST API.
        :return: Данные динамической аналитики или сообщение об ошибке.
        """
        user = self.request.user
        serializer = AnalyticsDynamicSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]

            filters = Q(establishment__owner=user)
            if start_date and end_date:
                filters &= Q(reservation_date__range=[start_date, end_date])

            total_reservation = ReservationHistory.objects.filter(
                filters,
                establishment=establishment_id,
            ).count()

            daily_reservations_by_day = (
                ReservationHistory.objects.filter(
                    filters,
                    establishment=establishment_id,
                )
                .values("reservation_date__date")
                .annotate(reservation_count=Count("id"))
            )

            monthly_reservations_by_month = (
                ReservationHistory.objects.filter(
                    filters,
                    establishment=establishment_id,
                )
                .annotate(month=ExtractMonth("reservation_date"))
                .values("month")
                .annotate(monthly_count=Count("id"))
            )

            yearly_reservation = (
                ReservationHistory.objects.filter(
                    filters,
                    establishment=establishment_id,
                )
                .values(
                    "reservation_date__year",
                )
                .annotate(yearly_count=Count("id"))
            )

            aggregated_data = {
                "total_reservation": total_reservation,
                "daily_reservations_by_day": list(daily_reservations_by_day),
                "monthly_reservations_by_month": list(
                    monthly_reservations_by_month
                ),
                "yearly_reservation": list(yearly_reservation),
            }

            serializer = AnalyticsDynamicSerializer(aggregated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_message = (
                "Некорректные данные. Пожалуйста, проверьте запрос."
            )
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Бизнес(аналитика заведения)"],
    description="Ресторатор",
    methods=["GET", "POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Аналитика бронирования за выбранное время",
    ),
    get=extend_schema(
        summary="Аналитика бронирования за день, неделю и год",
    ),
)
class AnalyticsViewSet(APIView):
    """
    Аналитика для 1 заведения.

    API endpoint для получения аналитики по бронированиям для определенного заведения.
    Предоставляет информацию о количестве бронирований по дням, неделям, месяцам и годам.

    Разрешения:
        - Только аутентифицированным пользователям (IsAuthenticated).
        - Пользователям, являющимся владельцами заведения (IsRestorateur).

    HTTP-методы:
        - GET: Получение статистики по бронированиям для определенного заведения.

    Параметры:
        - establishment_id: Идентификатор заведения для получения аналитики.

    """

    permission_classes = (IsAuthenticated, IsRestorateur)

    @extend_schema(
        responses=AnalyticsStaticSerializer,
    )
    def get(self, request, establishment_id):
        """
        Получение аналитики по бронированиям для определенного заведения.

        :param request: Объект запроса REST API.
        :param establishment_id: Идентификатор заведения для получения аналитики.
        :return: Данные аналитики по бронированиям для заведения или сообщение об ошибке.
        """
        establishment = Establishment.objects.get(pk=establishment_id)
        if request.user != establishment.owner:
            raise PermissionDenied(
                "Вы не являетесь владельцем этого заведения"
            )

        now_date = datetime.now().date()

        total_reservation = Reservation.objects.filter(
            establishment=establishment_id
        ).count()

        daily_reservation = Reservation.objects.filter(
            establishment=establishment_id,
            reservation_date__year=now_date.year,
            reservation_date__month=now_date.month,
            reservation_date__day=now_date.day,
        ).count()

        weekly_reservation = Reservation.objects.filter(
            establishment=establishment_id,
            reservation_date__week=ExtractWeek(now_date),
        ).count()

        monthly_reservation = (
            Reservation.objects.filter(
                establishment=establishment_id,
                reservation_date__year=now_date.year,
            )
            .annotate(month=ExtractMonth("reservation_date"))
            .values("month")
            .annotate(monthly_count=Count("id"))
        )

        yearly_reservation = (
            Reservation.objects.filter(
                establishment=establishment_id,
                reservation_date__year=now_date.year,
            )
            .values(
                "reservation_date__year",
            )
            .annotate(yearly_count=Count("id"))
        )

        daily_reservations_by_day = (
            Reservation.objects.filter(
                establishment=establishment_id,
            )
            .values("reservation_date__date")
            .annotate(reservation_count=Count("id"))
        )

        aggregated_data = {
            "total_reservation": total_reservation,
            "daily_reservation": daily_reservation,
            "weekly_reservation": weekly_reservation,
            "monthly_reservation": list(monthly_reservation),
            "yearly_reservation": yearly_reservation,
            "daily_reservations_by_day": list(daily_reservations_by_day),
        }

        serializer = AnalyticsStaticSerializer(aggregated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses=AnalyticsDynamicSerializer,
        request=AnalyticsDynamicSerializer,
    )
    def post(self, request, establishment_id):
        """
        Получение динамической аналитики по POST запросу.

        :param request: Объект запроса REST API.
        :return: Данные динамической аналитики или сообщение об ошибке.
        """
        user = self.request.user
        serializer = AnalyticsDynamicSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]

            filters = Q(establishment__owner=user)
            if start_date and end_date:
                filters &= Q(reservation_date__range=[start_date, end_date])

            total_reservation = Reservation.objects.filter(
                filters,
                establishment=establishment_id,
            ).count()

            daily_reservations_by_day = (
                Reservation.objects.filter(
                    filters,
                    establishment=establishment_id,
                )
                .values("reservation_date__date")
                .annotate(reservation_count=Count("id"))
            )

            monthly_reservations_by_month = (
                Reservation.objects.filter(
                    filters,
                    establishment=establishment_id,
                )
                .annotate(month=ExtractMonth("reservation_date"))
                .values("month")
                .annotate(monthly_count=Count("id"))
            )

            yearly_reservation = (
                Reservation.objects.filter(
                    filters,
                    establishment=establishment_id,
                )
                .values(
                    "reservation_date__year",
                )
                .annotate(yearly_count=Count("id"))
            )

            aggregated_data = {
                "total_reservation": total_reservation,
                "daily_reservations_by_day": list(daily_reservations_by_day),
                "monthly_reservations_by_month": list(
                    monthly_reservations_by_month
                ),
                "yearly_reservation": list(yearly_reservation),
            }

            serializer = AnalyticsDynamicSerializer(aggregated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_message = (
                "Некорректные данные. Пожалуйста, проверьте запрос."
            )
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Бизнес(аналитика полная)"],
    description="Ресторатор",
    methods=["GET", "POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Получить историю бронирования за выбранное время",
    ),
    get=extend_schema(
        summary="Получить историю бронирования за день, неделю и год",
    ),
)
class AnalyticsHistoryListViewSet(APIView):
    """
    Общая аналитика по всем заведениям.

    Этот класс предоставляет общую аналитику для пользователей со статусом 'is_restorateur'.
    """

    permission_classes = (IsAuthenticated, IsRestorateur)

    @extend_schema(
        responses=AnalyticsStaticSerializer,
    )
    def get(self, request):
        """
        Получение статической аналитики по GET запросу.

        :param request: Объект запроса REST API.
        :return: Данные статической аналитики.
        """
        user = self.request.user
        now_date = now().date()

        filters = {"establishment__owner": user}
        total_reservation = ReservationHistory.objects.filter(
            **filters
        ).count()

        daily_reservation = ReservationHistory.objects.filter(
            **filters,
            reservation_date__year=now_date.year,
            reservation_date__month=now_date.month,
            reservation_date__day=now_date.day,
        ).count()

        weekly_reservation = ReservationHistory.objects.filter(
            **filters,
            reservation_date__week=ExtractWeek(now_date),
        ).count()

        monthly_reservation = (
            ReservationHistory.objects.filter(
                **filters,
                reservation_date__year=now_date.year,
            )
            .annotate(month=ExtractMonth("reservation_date"))
            .values("month")
            .annotate(monthly_count=Count("id"))
        )

        yearly_reservation = (
            ReservationHistory.objects.filter(
                **filters, reservation_date__year=now_date.year
            )
            .values(
                "reservation_date__year",
            )
            .annotate(yearly_count=Count("id"))
        )

        daily_reservations_by_day = (
            ReservationHistory.objects.filter(
                **filters,
            )
            .values("reservation_date__date")
            .annotate(reservation_count=Count("id"))
        )

        aggregated_data = {
            "total_reservation": total_reservation,
            "daily_reservation": daily_reservation,
            "weekly_reservation": weekly_reservation,
            "monthly_reservation": list(monthly_reservation),
            "yearly_reservation": yearly_reservation,
            "daily_reservations_by_day": list(daily_reservations_by_day),
        }

        serializer = AnalyticsStaticSerializer(aggregated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses=AnalyticsDynamicSerializer,
        request=AnalyticsDynamicSerializer,
    )
    def post(self, request):
        """
        Получение динамической аналитики по POST запросу.

        :param request: Объект запроса REST API.
        :return: Данные динамической аналитики или сообщение об ошибке.
        """

        user = self.request.user
        serializer = AnalyticsDynamicSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]

            filters = {"establishment__owner": user}
            if start_date and end_date:
                filters["reservation_date__range"] = [start_date, end_date]

            total_reservation = ReservationHistory.objects.filter(
                **filters
            ).count()

            daily_reservations_by_day = (
                ReservationHistory.objects.filter(**filters)
                .values("reservation_date__date")
                .annotate(reservation_count=Count("id"))
            )

            monthly_reservations_by_month = (
                ReservationHistory.objects.filter(**filters)
                .annotate(month=ExtractMonth("reservation_date"))
                .values("month")
                .annotate(monthly_count=Count("id"))
            )

            yearly_reservation = (
                ReservationHistory.objects.filter(**filters)
                .values(
                    "reservation_date__year",
                )
                .annotate(yearly_count=Count("id"))
            )

            aggregated_data = {
                "total_reservation": total_reservation,
                "daily_reservations_by_day": list(daily_reservations_by_day),
                "monthly_reservations_by_month": list(
                    monthly_reservations_by_month
                ),
                "yearly_reservation": list(yearly_reservation),
            }

            serializer = AnalyticsDynamicSerializer(aggregated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_message = (
                "Некорректные данные. Пожалуйста, проверьте запрос."
            )
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Бизнес(аналитика полная)"],
    description="Ресторатор",
    methods=["GET", "POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Аналитика бронирования за выбранное время",
    ),
    get=extend_schema(
        summary="Аналитика бронирования за день, неделю и год",
    ),
)
class AnalyticsListViewSet(APIView):
    """
    Общая аналитика по всем заведениям.

    Этот класс предоставляет общую аналитику для пользователей со статусом 'is_restorateur'.
    """

    permission_classes = (IsAuthenticated, IsRestorateur)

    @extend_schema(
        responses=AnalyticsStaticSerializer,
    )
    def get(self, request):
        """
        Получение статической аналитики по GET запросу.

        :param request: Объект запроса REST API.
        :return: Данные статической аналитики.
        """
        user = self.request.user
        now_date = now().date()

        filters = {"establishment__owner": user}
        total_reservation = Reservation.objects.filter(**filters).count()

        daily_reservation = Reservation.objects.filter(
            **filters,
            reservation_date__year=now_date.year,
            reservation_date__month=now_date.month,
            reservation_date__day=now_date.day,
        ).count()

        weekly_reservation = Reservation.objects.filter(
            **filters,
            reservation_date__week=ExtractWeek(now_date),
        ).count()

        monthly_reservation = (
            Reservation.objects.filter(
                **filters,
                reservation_date__year=now_date.year,
            )
            .annotate(month=ExtractMonth("reservation_date"))
            .values("month")
            .annotate(monthly_count=Count("id"))
        )

        yearly_reservation = (
            Reservation.objects.filter(
                **filters, reservation_date__year=now_date.year
            )
            .values(
                "reservation_date__year",
            )
            .annotate(yearly_count=Count("id"))
        )

        daily_reservations_by_day = (
            Reservation.objects.filter(
                **filters,
            )
            .values("reservation_date__date")
            .annotate(reservation_count=Count("id"))
        )

        aggregated_data = {
            "total_reservation": total_reservation,
            "daily_reservation": daily_reservation,
            "weekly_reservation": weekly_reservation,
            "monthly_reservation": list(monthly_reservation),
            "yearly_reservation": yearly_reservation,
            "daily_reservations_by_day": list(daily_reservations_by_day),
        }

        serializer = AnalyticsStaticSerializer(aggregated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses=AnalyticsDynamicSerializer,
        request=AnalyticsDynamicSerializer,
    )
    def post(self, request):
        """
        Получение динамической аналитики по POST запросу.

        :param request: Объект запроса REST API.
        :return: Данные динамической аналитики или сообщение об ошибке.
        """

        user = self.request.user
        serializer = AnalyticsDynamicSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]

            filters = {"establishment__owner": user}
            if start_date and end_date:
                filters["reservation_date__range"] = [start_date, end_date]

            total_reservation = Reservation.objects.filter(**filters).count()

            daily_reservations_by_day = (
                Reservation.objects.filter(**filters)
                .values("reservation_date__date")
                .annotate(reservation_count=Count("id"))
            )

            monthly_reservations_by_month = (
                Reservation.objects.filter(**filters)
                .annotate(month=ExtractMonth("reservation_date"))
                .values("month")
                .annotate(monthly_count=Count("id"))
            )

            yearly_reservation = (
                Reservation.objects.filter(**filters)
                .values(
                    "reservation_date__year",
                )
                .annotate(yearly_count=Count("id"))
            )

            aggregated_data = {
                "total_reservation": total_reservation,
                "daily_reservations_by_day": list(daily_reservations_by_day),
                "monthly_reservations_by_month": list(
                    monthly_reservations_by_month
                ),
                "yearly_reservation": list(yearly_reservation),
            }

            serializer = AnalyticsDynamicSerializer(aggregated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_message = (
                "Некорректные данные. Пожалуйста, проверьте запрос."
            )
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now

from api.permissions import IsRestorateur
from api.serializers.analytics import (
    AnalyticsStaticSerializer,
    AnalyticsDynamicSerializer,
)
from reservation.models import Reservation, ReservationHistory
from rest_framework.response import Response


@extend_schema(
    tags=["Бизнес(аналитика заведения)"],
    description="Ресторатор",
    methods=["GET", "POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Получить бронирования за выбранное время",
    ),
    get=extend_schema(
        summary="Аналитика за день, неделю и год",
    ),
)
class AnalyticsViewSet(APIView):
    """Аналитика для 1 здаведения"""

    @extend_schema(
        responses=AnalyticsStaticSerializer,
    )
    def get(self, request, establishment_id):
        total_reservation = Reservation.objects.filter(
            establishment=establishment_id
        ).count()
        daily_reservation = Reservation.objects.filter(
            establishment=establishment_id, reservation_date__date=now().date()
        ).count()
        weekly_reservation = Reservation.objects.filter(
            establishment=establishment_id,
            reservation_date__week=now().isocalendar()[1],
        ).count()
        yearly_reservation = Reservation.objects.filter(
            establishment=establishment_id, reservation_date__year=now().year
        ).count()
        aggregated_data = {
            "total_reservation": total_reservation,
            "daily_reservation": daily_reservation,
            "weekly_reservation": weekly_reservation,
            "yearly_reservation": yearly_reservation,
        }
        serializer = AnalyticsStaticSerializer(aggregated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses=AnalyticsDynamicSerializer,
        request=AnalyticsDynamicSerializer,
    )
    def post(self, request, establishment_id):
        serializer = AnalyticsDynamicSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data.get("start_date")
            end_date = serializer.validated_data.get("end_date")
            analytics_serializer = AnalyticsDynamicSerializer()
            total_reservation = analytics_serializer.get_reservation_analytics(
                start_date, end_date, establishment_id
            )
            return Response({"total_reservation": total_reservation})
        # def post(self, request, establishment_id):
        #     serializer = AnalyticsDynamicSerializer(data=request.data)
        #     if serializer.is_valid():
        #         start_date = serializer.validated_data["start_date"]
        #         end_date = serializer.validated_data["end_date"]
        #         total_reservation = Reservation.objects.filter(
        #             establishment=establishment_id,
        #             reservation_date__range=[start_date, end_date],
        #         ).count()
        #
        #         aggregated_data = {
        #             "total_reservation": total_reservation,
        #         }
        #         serializer = AnalyticsDynamicSerializer(aggregated_data)
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Бизнес(аналитика полная)"],
    description="Ресторатор",
    methods=["GET", "POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Получить бронирования за выбранное время",
    ),
    get=extend_schema(
        summary="Аналитика за день, неделю и год",
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
        aggregated_data = self._get_aggregated_data(user=user)
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
            aggregated_data = self._get_aggregated_data(
                user=user, start_date=start_date, end_date=end_date
            )
            serializer = AnalyticsDynamicSerializer(aggregated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_message = (
                "Некорректные данные. Пожалуйста, проверьте запрос."
            )
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )

    def _get_aggregated_data(self, user, start_date=None, end_date=None):
        """
        Получение агрегированных данных по бронированиям.

        :param user: Пользователь для фильтрации данных.
        :param start_date: Начальная дата для фильтрации (необязательно).
        :param end_date: Конечная дата для фильтрации (необязательно).
        :return: Словарь с агрегированными данными по бронированиям.
        """
        filters = {"establishment__owner": user}
        if start_date and end_date:
            filters["reservation_date__range"] = [start_date, end_date]

        total_reservation = ReservationHistory.objects.filter(
            **filters
        ).count()
        daily_reservation = ReservationHistory.objects.filter(
            **filters, reservation_date__date=now().date()
        ).count()
        weekly_reservation = ReservationHistory.objects.filter(
            **filters, reservation_date__week=now().isocalendar()[1]
        ).count()
        yearly_reservation = ReservationHistory.objects.filter(
            **filters, reservation_date__year=now().year
        ).count()

        return {
            "total_reservation": total_reservation,
            "daily_reservation": daily_reservation,
            "weekly_reservation": weekly_reservation,
            "yearly_reservation": yearly_reservation,
        }

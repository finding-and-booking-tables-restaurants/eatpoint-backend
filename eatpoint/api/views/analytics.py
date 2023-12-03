from datetime import timedelta

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import ExtractMonth


from api.permissions import IsRestorateur
from api.serializers.analytics import (
    AnalyticsStaticSerializer,
    AnalyticsDynamicSerializer,
)
from establishments.models import Establishment
from reservation.models import ReservationHistory
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
        summary="Аналитика за день, неделю и год",
    ),
)
class AnalyticsViewSet(APIView):
    """Аналитика для 1 заведения"""

    permission_classes = (IsAuthenticated, IsRestorateur)

    @extend_schema(
        responses=AnalyticsStaticSerializer,
    )
    def get(self, request, establishment_id):
        establishment = Establishment.objects.get(pk=establishment_id)
        if request.user != establishment.owner:
            raise PermissionDenied(
                "Вы не являетесь владельцем этого заведения"
            )

        total_reservation = ReservationHistory.objects.filter(
            establishment=establishment_id
        ).count()
        daily_reservation = ReservationHistory.objects.filter(
            establishment=establishment_id, reservation_date__date=now().date()
        ).count()
        weekly_reservation = ReservationHistory.objects.filter(
            establishment=establishment_id,
            reservation_date__week=now().isocalendar()[1],
        ).count()

        monthly_reservation = (
            ReservationHistory.objects.filter(
                establishment=establishment_id,
                reservation_date__year=now().year,
            )
            .annotate(month=ExtractMonth("reservation_date"))
            .values("month")
            .annotate(monthly_count=Count("id"))
        )

        daily_reservations_last_week = (
            ReservationHistory.objects.filter(
                establishment=establishment_id,
                reservation_date__date__range=[
                    now().date() - timedelta(days=6),
                    now().date() + timedelta(days=1),
                ],
            )
            .values("reservation_date__date")
            .annotate(reservation_count=Count("id"))
        )

        yearly_reservation = ReservationHistory.objects.filter(
            establishment=establishment_id, reservation_date__year=now().year
        ).count()

        aggregated_data = {
            "total_reservation": total_reservation,
            "daily_reservation": daily_reservation,
            "weekly_reservation": weekly_reservation,
            "monthly_reservation": list(monthly_reservation),
            "daily_reservations_last_week": list(daily_reservations_last_week),
            "yearly_reservation": yearly_reservation,
        }
        serializer = AnalyticsStaticSerializer(aggregated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses=AnalyticsDynamicSerializer,
        request=AnalyticsDynamicSerializer,
    )
    # def post(self, request, establishment_id):
    #     serializer = AnalyticsDynamicSerializer(data=request.data)
    #     if serializer.is_valid():
    #         start_date = serializer.validated_data["start_date"]
    #         end_date = serializer.validated_data["end_date"]
    #
    #         total_reservation = ReservationHistory.objects.filter(
    #             establishment=establishment_id,
    #             reservation_date__range=[start_date, end_date],
    #         ).count()
    #         reservations_by_day = ReservationHistory.objects.filter(
    #             establishment=establishment_id,
    #             reservation_date__range=[start_date, end_date],
    #         ).values('reservation_date__date').annotate(reservation_count=Count('id'))
    #
    #         # Преобразовать QuerySet в список словарей для сериализации
    #         reservations_by_day_list = list(reservations_by_day)
    #
    #         aggregated_data = {
    #             "total_reservation": total_reservation,
    #             "reservations_by_day": reservations_by_day_list,
    #             # Можете добавить другие данные здесь, если необходимо
    #         }
    #
    #         serializer = AnalyticsDynamicSerializer(aggregated_data)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

            filters = {"establishment__owner": user}
            if start_date and end_date:
                filters["reservation_date__range"] = [start_date, end_date]

            total_reservation = ReservationHistory.objects.filter(
                **filters
            ).count()

            daily_reservations = (
                ReservationHistory.objects.filter(
                    establishment=establishment_id,
                    reservation_date__date=start_date,
                )
                .values("reservation_date__date")
                .annotate(reservation_count=Count("id"))
            )
            daily_reservations_list = list(daily_reservations)
            if not daily_reservations_list:
                daily_reservations_list.append(
                    {
                        "reservation_date__date": start_date,
                        "reservation_count": 0,
                    }
                )

            daily_reservations_last_week = (
                ReservationHistory.objects.filter(
                    establishment=establishment_id,
                    reservation_date__range=[start_date, end_date],
                )
                .values("reservation_date__date")
                .annotate(reservation_count=Count("id"))
            )
            daily_reservations_last_week_list = list(
                daily_reservations_last_week
            )

            monthly_reservations = (
                ReservationHistory.objects.filter(
                    establishment=establishment_id, **filters
                )
                .annotate(month=ExtractMonth("reservation_date"))
                .values("month")
                .annotate(monthly_count=Count("id"))
            )
            monthly_reservations_list = [
                {
                    "month": entry["month"],
                    "monthly_count": entry["monthly_count"],
                }
                for entry in monthly_reservations
            ]
            monthly_reservations_list = [
                entry
                for entry in monthly_reservations_list
                if entry["monthly_count"] > 0
            ]
            monthly_reservations_list = sorted(
                monthly_reservations_list, key=lambda x: x["month"]
            )

            aggregated_data = {
                "total_reservation": total_reservation,
                "daily_reservations": daily_reservations_list,
                "daily_reservations_last_week": daily_reservations_last_week_list,
                "monthly_reservations": monthly_reservations_list,
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
        now_date = now().date()

        filters = {"establishment__owner": user}
        total_reservation = ReservationHistory.objects.filter(
            **filters
        ).count()

        daily_reservation = ReservationHistory.objects.filter(
            **filters, reservation_date__date=now_date
        ).count()

        weekly_reservation = ReservationHistory.objects.filter(
            **filters, reservation_date__week=now().isocalendar()[1]
        ).count()

        monthly_reservation = (
            ReservationHistory.objects.filter(**filters)
            .annotate(month=ExtractMonth("reservation_date"))
            .values("month")
            .annotate(monthly_count=Count("id"))
        )

        daily_reservations_last_week = (
            ReservationHistory.objects.filter(
                **filters,
                reservation_date__date__range=[
                    now_date - timedelta(days=6),
                    now_date + timedelta(days=1),
                ],
            )
            .values("reservation_date__date")
            .annotate(reservation_count=Count("id"))
        )

        yearly_reservation = ReservationHistory.objects.filter(
            **filters, reservation_date__year=now().year
        ).count()

        aggregated_data = {
            "total_reservation": total_reservation,
            "daily_reservation": daily_reservation,
            "weekly_reservation": weekly_reservation,
            "daily_reservations_last_week": list(daily_reservations_last_week),
            "monthly_reservation": list(monthly_reservation),
            "yearly_reservation": yearly_reservation,
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

            daily_reservations = (
                ReservationHistory.objects.filter(
                    reservation_date__date=start_date
                )
                .values("reservation_date__date")
                .annotate(reservation_count=Count("id"))
            )
            daily_reservations_list = list(daily_reservations)
            if not daily_reservations_list:
                daily_reservations_list.append(
                    {
                        "reservation_date__date": start_date,
                        "reservation_count": 0,
                    }
                )

            daily_reservations_last_week = (
                ReservationHistory.objects.filter(
                    reservation_date__range=[start_date, end_date],
                )
                .values("reservation_date__date")
                .annotate(reservation_count=Count("id"))
            )
            daily_reservations_last_week_list = list(
                daily_reservations_last_week
            )

            monthly_reservations = (
                ReservationHistory.objects.filter(**filters)
                .annotate(month=ExtractMonth("reservation_date"))
                .values("month")
                .annotate(monthly_count=Count("id"))
            )
            monthly_reservations_list = [
                {
                    "month": entry["month"],
                    "monthly_count": entry["monthly_count"],
                }
                for entry in monthly_reservations
            ]
            monthly_reservations_list = [
                entry
                for entry in monthly_reservations_list
                if entry["monthly_count"] > 0
            ]
            monthly_reservations_list = sorted(
                monthly_reservations_list, key=lambda x: x["month"]
            )

            aggregated_data = {
                "total_reservation": total_reservation,
                "daily_reservations": daily_reservations_list,
                "daily_reservations_last_week": daily_reservations_last_week_list,
                "monthly_reservations": monthly_reservations_list,
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

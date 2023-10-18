from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.views import APIView
from django.utils.timezone import now
from api.serializers.analytics import (
    AnalyticsStaticSerializer,
    AnalyticsDynamicSerializer,
)
from reservation.models import Reservation
from rest_framework.response import Response


@extend_schema(
    tags=["Аналитика(заведение)"],
    description="Аналитика для 1 заведения ресторатора",
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
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            total_reservation = Reservation.objects.filter(
                establishment=establishment_id,
                reservation_date__range=[start_date, end_date],
            ).count()

            aggregated_data = {
                "total_reservation": total_reservation,
            }
            serializer = AnalyticsDynamicSerializer(aggregated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Аналитика(полная)"],
    description="Аналитика для всех заведений ресторатора",
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
    """Общая аналитика по всем заведениям"""

    @extend_schema(
        responses=AnalyticsStaticSerializer,
    )
    def get(self, request):
        user = self.request.user
        total_reservation = Reservation.objects.filter(
            establishment__owner=user,
        ).count()
        daily_reservation = Reservation.objects.filter(
            establishment__owner=user, reservation_date__date=now().date()
        ).count()
        weekly_reservation = Reservation.objects.filter(
            establishment__owner=user,
            reservation_date__week=now().isocalendar()[1],
        ).count()
        yearly_reservation = Reservation.objects.filter(
            establishment__owner=user, reservation_date__year=now().year
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
    def post(self, request):
        user = self.request.user
        serializer = AnalyticsDynamicSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            total_reservation = Reservation.objects.filter(
                establishment__owner=user,
                reservation_date__range=[start_date, end_date],
            ).count()

            aggregated_data = {
                "total_reservation": total_reservation,
            }
            serializer = AnalyticsDynamicSerializer(aggregated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

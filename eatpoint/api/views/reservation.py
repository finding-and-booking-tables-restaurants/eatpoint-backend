from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from establishments.models import Establishment
from api.serializers.reservations import ReservationsEditSerializer

# Create your views here.


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
    ),
    partial_update=extend_schema(
        summary="Изменить данные бронирования",
    ),
    destroy=extend_schema(
        summary="Удалить бронирование",
    ),
)
class ReservationsViewSet(viewsets.ModelViewSet):
    """Вьюсет  для обработки бронирования"""

    serializer_class = ReservationsEditSerializer
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        return establishment.reservation.all()

    def perform_create(self, serializer):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
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

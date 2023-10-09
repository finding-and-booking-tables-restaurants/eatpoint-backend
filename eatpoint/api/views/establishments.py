from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from api.serializers.establishments import (
    EstablishmentSerializer,
    ReviewSerializer,
)
from establishments.models import Establishment


@extend_schema(tags=["Заведения"], methods=["GET"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список заведений",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о заведении",
    ),
)
class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    http_method_names = ["get"]


@extend_schema(tags=["Отзывы"], methods=["GET", "POST", "PATCH"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список отзывов к заведению с id=",
    ),
    create=extend_schema(summary="Оставить отзыв"),
    retrieve=extend_schema(
        summary="Один отзыв",
    ),
    partial_update=extend_schema(
        summary="Редактировать отзыв",
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        return establishment.review.all()

    def perform_create(self, serializer):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        serializer.save(author=self.request.user, establishment=establishment)

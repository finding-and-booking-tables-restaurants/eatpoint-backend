from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)
from rest_framework import generics, viewsets
from api.permissions import IsAuthor, IsEstablishmentOwner, ReadOnly
from api.v2.serializers.reviews import (
    OwnerResponseSerializer,
    ReviewSerializer,
)

from establishments.models import Establishment
from reviews.models import Review


@extend_schema(
    tags=["Отзывы"],
    methods=["GET", "POST", "PATCH", "DELETE"],
    description="Клиент",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список отзывов к заведению с id=",
        description="Клиент/ресторатор",
    ),
    destroy=extend_schema(
        summary="Удалить отзыв",
        description="Клиент/ресторатор",
    ),
    create=extend_schema(summary="Оставить отзыв"),
    retrieve=extend_schema(
        summary="Один отзыв",
        description="Клиент/ресторатор",
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
    partial_update=extend_schema(
        summary="Редактировать отзыв",
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
class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет: Отзывы"""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthor | ReadOnly,)
    http_method_names = ["get", "patch", "delete", "post"]

    def get_queryset(self):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        return establishment.review.all()

    def perform_create(self, serializer):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        serializer.save(author=self.request.user, establishment=establishment)


@extend_schema(
    tags=["Ответы владельца заведения"],
    methods=["POST"],
    description="Добавление ответа владельца заведения к отзыву",
)
class OwnerResponseCreateView(generics.CreateAPIView):
    """Вьюсет: Отзывы(владелец заведения)"""

    serializer_class = OwnerResponseSerializer
    permission_classes = (IsEstablishmentOwner,)

    @extend_schema(
        request=OwnerResponseSerializer,
        responses={201: OwnerResponseSerializer},
    )
    def perform_create(self, serializer):
        """Получаем отзыв_id из URL"""
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, establishment_owner=self.request.user)

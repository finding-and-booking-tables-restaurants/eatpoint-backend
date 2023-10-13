from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)
from rest_framework import viewsets, status, filters
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action

from api.filters.establishments import (
    EstablishmentFilterBackend,
    TypeEstFilterBackend,
    ServicesEstFilterBackend,
)
from api.permissions import ReadOnly
from api.serializers.establishments import (
    EstablishmentSerializer,
    ReviewSerializer,
    EstablishmentEditSerializer,
    SpecialEstablishmentSerializer,
    KitchenSerializer,
    TypeEstSerializer,
    ServicesSerializer,
)
from establishments.models import (
    Establishment,
    Favorite,
    Kitchen,
    TypeEst,
    Service,
)


@extend_schema(tags=["Кухни"], methods=["GET"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список кухонь",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о кухне",
    ),
)
class KitchenViewSet(viewsets.ModelViewSet):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer
    permission_classes = (ReadOnly,)
    http_method_names = ["get"]


@extend_schema(tags=["Типы заведения"], methods=["GET"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список типов заведений",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о типе заведения",
    ),
)
class TypeEstViewSet(viewsets.ModelViewSet):
    queryset = TypeEst.objects.all()
    serializer_class = TypeEstSerializer
    permission_classes = (ReadOnly,)
    http_method_names = ["get"]


@extend_schema(tags=["Доп. услуги"], methods=["GET"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список услуг",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о услуге",
    ),
)
class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = (ReadOnly,)
    http_method_names = ["get"]


@extend_schema(tags=["Заведения"], methods=["GET"])
@extend_schema(tags=["Бизнес"], methods=["POST", "PATCH", "PUT", "DELETE"])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name="kitchens", description="Кухня заведения"),
            OpenApiParameter(name="types", description="Тип заведения"),
            OpenApiParameter(name="services", description="Доп. услуги"),
        ],
        summary="Получить список заведений",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о заведении",
    ),
    create=extend_schema(
        summary="Добавить заведение",
    ),
    partial_update=extend_schema(
        summary="Изменить данные заведения",
    ),
    destroy=extend_schema(
        summary="Удалить заведение",
    ),
    update=extend_schema(summary="Изменить заведение [PUT]"),
)
class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    filter_backends = (
        EstablishmentFilterBackend,
        TypeEstFilterBackend,
        ServicesEstFilterBackend,
        filters.SearchFilter,
    )
    search_fields = {
        "name",
        "address",
        "kitchens__name",
        "types__name",
    }

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return EstablishmentSerializer
        return EstablishmentEditSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def __added(self, model, user, pk, name):
        establishment = get_object_or_404(Establishment, id=pk)
        if model.objects.filter(
            user=user, establishment=establishment
        ).exists():
            return Response(
                {"errors": f"Вы уже добавили {establishment.name} в {name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.create(user=user, establishment=establishment)
        serializer = SpecialEstablishmentSerializer(establishment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def __deleted(self, model, user, pk, name):
        establishment = get_object_or_404(Establishment, id=pk)
        removable = model.objects.filter(
            user=user, establishment=establishment
        )
        if not removable.exists():
            return Response(
                {"errors": f"Вы не добавляли {establishment.name} в {name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        removable.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        tags=["Избранное"],
        methods=["POST"],
        request=SpecialEstablishmentSerializer,
        responses=SpecialEstablishmentSerializer,
        summary="Добавить в избранное",
    )
    @extend_schema(
        tags=["Избранное"],
        methods=["DELETE"],
        summary="Удалить из избранного",
    )
    @action(
        detail=True,
        methods=["post", "delete"],
        url_path="favorite",
    )
    def favorite(self, request, pk=None):
        name = "избранное"
        user = request.user
        if request.method == "POST":
            return self.__added(Favorite, user, pk, name)
        if request.method == "DELETE":
            return self.__deleted(Favorite, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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

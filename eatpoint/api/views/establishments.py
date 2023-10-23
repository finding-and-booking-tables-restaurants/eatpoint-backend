from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets, status
from rest_framework.permissions import SAFE_METHODS, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from api.filters.establishments import (
    EstablishmentFilter,
    CityFilter,
)
from api.permissions import (
    ReadOnly,
    IsAuthor,
    IsClient,
    IsRestorateur,
)
from api.serializers.establishments import (
    EstablishmentSerializer,
    ReviewSerializer,
    EstablishmentEditSerializer,
    KitchenSerializer,
    TypeEstSerializer,
    ServicesSerializer,
    ZoneEstablishmentSerializer,
    CitySerializer,
)
from api.serializers.reservations import SpecialEstablishmentSerializer
from core.pagination import LargeResultsSetPagination
from establishments.models import (
    Establishment,
    Favorite,
    Kitchen,
    TypeEst,
    Service,
    ZoneEstablishment,
    City,
)


@extend_schema(
    tags=["Кухни"],
    methods=["GET"],
    description="Все пользователи",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список кухонь",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о кухне",
    ),
)
class KitchenViewSet(viewsets.ModelViewSet):
    """Вьюсет: Кухня"""

    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer
    http_method_names = ["get"]


@extend_schema(
    tags=["Список городов"],
    methods=["GET"],
    description="Все пользователи",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список городов",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о городе",
    ),
)
class CityViewSet(viewsets.ModelViewSet):
    """Вьюсет: Город"""

    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = ["get"]
    filter_backends = [CityFilter]
    search_fields = ("name",)


@extend_schema(
    tags=["Типы заведения"],
    methods=["GET"],
    description="Все пользователи",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список типов заведений",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о типе заведения",
    ),
)
class TypeEstViewSet(viewsets.ModelViewSet):
    """Вьюсет: Тип заведения"""

    queryset = TypeEst.objects.all()
    serializer_class = TypeEstSerializer
    http_method_names = ["get"]


@extend_schema(
    tags=["Доп. услуги"],
    methods=["GET"],
    description="Все пользователи",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список услуг",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о услуге",
    ),
)
class ServicesViewSet(viewsets.ModelViewSet):
    """Вьюсет: Доп. услуги"""

    queryset = Service.objects.all()
    serializer_class = ServicesSerializer
    http_method_names = ["get"]


@extend_schema(
    tags=["Бизнес(заведения)"],
    methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    description="Ресторатор",
)
@extend_schema_view(
    list=extend_schema(
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
class EstablishmentBusinessViewSet(viewsets.ModelViewSet):
    """Вьюсет: Заведение(для бизнеса)"""

    filterset_class = EstablishmentFilter
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsRestorateur,)
    search_fields = (
        "$name",
        "$address",
        "$kitchens__name",
        "$types__name",
    )

    def get_queryset(self):
        user = self.request.user
        return Establishment.objects.filter(owner=user)

    def get_serializer_class(self):
        """Выбор serializer_class в зависимости от типа запроса"""
        if self.request.method in SAFE_METHODS:
            return EstablishmentSerializer
        return EstablishmentEditSerializer

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
        )


@extend_schema(
    tags=["Заведения"],
    methods=["GET"],
    description="Все пользователи",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список заведений",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о заведении",
    ),
)
class EstablishmentViewSet(viewsets.ModelViewSet):
    """Вьюсет: Заведение"""

    queryset = Establishment.objects.filter(is_verified=True)
    filterset_class = EstablishmentFilter
    pagination_class = LargeResultsSetPagination
    permission_classes = (ReadOnly | IsAdminUser,)
    search_fields = (
        "$name",
        "$address",
        "$kitchens__name",
        "$types__name",
    )
    serializer_class = EstablishmentSerializer
    http_method_names = ("get",)

    def __added(self, model, user, pk, name):
        """Добавление(шаблон)"""
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
        """Удаление(шаблон)"""
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
        description="Клиент",
        methods=["POST"],
        request=SpecialEstablishmentSerializer,
        responses=SpecialEstablishmentSerializer,
        summary="Добавить в избранное",
    )
    @extend_schema(
        tags=["Избранное"],
        description="Клиент",
        methods=["DELETE"],
        summary="Удалить из избранного",
    )
    @action(
        detail=True,
        methods=["post", "delete"],
        url_path="favorite",
        filterset_class=EstablishmentFilter,
        permission_classes=(IsClient,),
    )
    def favorite(self, request, pk=None):
        """Добавление в избранное"""
        name = "избранное"
        user = request.user
        if request.method == "POST":
            return self.__added(Favorite, user, pk, name)
        if request.method == "DELETE":
            return self.__deleted(Favorite, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(
    tags=["Зоны"],
    methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    description="Все пользователи",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список зон к заведению с id=",
    ),
    create=extend_schema(summary="Добавить зону"),
    retrieve=extend_schema(
        summary="Одна зона",
    ),
    partial_update=extend_schema(
        summary="Редактировать зону",
        description="Ресторатор",
    ),
)
class ZoneViewSet(viewsets.ModelViewSet):
    """Вьюсет: Зоны заведения"""

    serializer_class = ZoneEstablishmentSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        establishment_id = self.kwargs["establishment_id"]
        return ZoneEstablishment.objects.filter(
            establishment_id=establishment_id
        )


@extend_schema(
    tags=["Отзывы"], methods=["GET", "POST", "PATCH"], description="Клиент"
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список отзывов к заведению с id=",
        description="Клиент/ресторатор",
    ),
    create=extend_schema(summary="Оставить отзыв"),
    retrieve=extend_schema(
        summary="Один отзыв",
        description="Клиент/ресторатор",
    ),
    partial_update=extend_schema(
        summary="Редактировать отзыв",
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет: Отзывы"""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthor | ReadOnly | IsAdminUser,)
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        return establishment.review.all()

    def perform_create(self, serializer):
        establishment_id = self.kwargs.get("establishment_id")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        serializer.save(author=self.request.user, establishment=establishment)

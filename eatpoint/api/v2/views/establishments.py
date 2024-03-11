from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters.establishments import (
    EstablishmentFilter,
    CityFilter,
)
from api.permissions import (
    ReadOnly,
    IsClient,
    IsRestorateur,
    IsRestorateurEdit,
)
from api.v2.serializers.establishments import (
    EstablishmentSerializer,
    EstablishmentEditSerializer,
    KitchenSerializer,
    TypeEstSerializer,
    ServicesSerializer,
    ZoneEstablishmentSerializer,
    CitySerializer,
    ImageSerializer,
)
from core.pagination import LargeResultsSetPagination
from establishments.models import (
    Establishment,
    Favorite,
    Kitchen,
    TypeEst,
    Service,
    ZoneEstablishment,
    City,
    ImageEstablishment,
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
    tags=["Изображения"],
    methods=["POST", "PATCH", "DELETE"],
    description="Хозяин заведения",
)
@extend_schema_view(
    create=extend_schema(
        summary="Создать изображения",
    ),
    partial_update=extend_schema(
        summary="Изменить изображения",
    ),
    destroy=extend_schema(summary="Удалить изображение"),
)
class ImageEstablishmentViewSet(viewsets.ModelViewSet):
    """Добавление и редактирование изображений"""

    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ("patch", "post", "delete")
    permission_classes = (IsRestorateurEdit,)

    def get_queryset(self):
        establishment_id = self.kwargs.get("establishment_id")
        images = ImageEstablishment.objects.filter(
            establishment=establishment_id
        )
        return images

    def create(self, request, *args, **kwargs):
        establishment_id = self.kwargs.get("establishment_id")
        instance = Establishment.objects.get(pk=establishment_id)
        print(self.request.FILES)
        images_data = self.request.FILES.getlist("image")
        if not images_data:
            return Response(
                {"detail": "Не было передано ни одного изображения"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = self.request.user
        if user == instance.owner:
            current_images_count = ImageEstablishment.objects.filter(
                establishment=instance
            ).count()
            max_images_count = 10

            if current_images_count + len(images_data) > max_images_count:
                return Response(
                    {"detail": "Слишком много"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for image_data in images_data:
                ImageEstablishment.objects.get_or_create(
                    establishment=instance,
                    image=image_data,
                    name=image_data.name,
                )

            return Response(
                {"detail": "Создано"}, status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_403_FORBIDDEN)


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
        return (
            Establishment.objects.filter(owner=user)
            .select_related("cities")
            .prefetch_related(
                "types",
                "kitchens",
                "services",
                "zones",
                "socials",
                "worked",
                "images",
                "review",
            )
        ).order_by("id")

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

    queryset = (
        Establishment.objects.filter(is_verified=True)
        .select_related("owner", "cities")
        .prefetch_related(
            "types",
            "kitchens",
            "services",
            "zones",
            "socials",
            "worked",
            "images",
            "review",
        )
    ).order_by("id")

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
    http_method_names = ["get"]


@extend_schema(
    tags=["Избранное"],
    methods=["POST", "DELETE"],
    description="Авторизованный",
)
@extend_schema_view(
    post=extend_schema(
        summary="Добавить в избранное",
    ),
    delete=extend_schema(
        summary="Удалить из избранного",
    ),
)
class FavoriteViewSet(APIView):
    """Избранное"""

    permission_classes = [IsClient]
    http_method_names = ["post", "delete"]

    def post(self, request, establishment_id):
        name = "избранное"
        user = request.user
        establishment = get_object_or_404(Establishment, id=establishment_id)
        if establishment.owner == user:
            return Response(
                {
                    "errors": f"Нельзя добавить своё заведение {establishment.name} в {name}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Favorite.objects.filter(
            user=user, establishment=establishment
        ).exists():
            return Response(
                {"errors": f"Вы уже добавили {establishment.name} в {name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Favorite.objects.create(user=user, establishment=establishment)
        return Response(
            {"errors": f"Вы добавили {establishment.name} в {name}"},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, establishment_id):
        name = "избранное"
        user = request.user
        establishment = get_object_or_404(Establishment, id=establishment_id)
        removable = Favorite.objects.filter(
            user=user, establishment=establishment
        )
        if not removable.exists():
            return Response(
                {"errors": f"Вы не добавляли {establishment.name} в {name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        removable.delete()
        return Response(
            {"errors": f"Вы удалили {establishment.name} из {name}"},
            status=status.HTTP_404_NOT_FOUND,
        )


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
        summary="Редактировать зону",
        description="Ресторатор",
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
class ZoneViewSet(viewsets.ModelViewSet):
    """Вьюсет: Зоны заведения"""

    serializer_class = ZoneEstablishmentSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        establishment_id = self.kwargs["establishment_id"]
        return ZoneEstablishment.objects.filter(
            establishment_id=establishment_id
        )

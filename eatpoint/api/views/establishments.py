from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from api.serializers.establishments import EstablishmentSerializer
from establishments.models import Establishment


@extend_schema(tags=["Establishment"], methods=["GET"])
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

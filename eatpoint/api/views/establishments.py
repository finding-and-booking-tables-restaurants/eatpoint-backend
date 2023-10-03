from rest_framework import viewsets

from api.serializers.establishments import EstablishmentSerializer
from establishments.models import Establishment


class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer

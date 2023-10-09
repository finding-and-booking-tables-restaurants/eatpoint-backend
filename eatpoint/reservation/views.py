from rest_framework import viewsets 
from .models import EstablishmentReserv
from api.serializers.reservations import ReservationsSerializer

# Create your views here.

# @action[GET, POST, DELETE, PUT]
class ReservationsViewSet(viewsets.ModelViewSet):
    """Вьюсет  для обработки бронирования"""
    queryset = EstablishmentReserv.objects.all()
    serializer_class = ReservationsSerializer
    

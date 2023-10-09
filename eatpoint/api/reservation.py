from rest_framework import viewsets 
from reservation.models import EstablishmentReserv
from api.serializers.reservations import ReservationsSerializer
from rest_framework.decorators import action
# Create your views here.

@action(methods=['get', 'delete', 'put']) 
class ReservationsViewSet(viewsets.ModelViewSet):
    """Вьюсет  для обработки бронирования"""
    queryset = EstablishmentReserv.objects.all()
    serializer_class = ReservationsSerializer
    

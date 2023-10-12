from rest_framework import viewsets
from .models import Reservation
from api.serializers.reservations import ReservationsEditSerializer

# Create your views here.


# @action[GET, POST, DELETE, PUT]
class ReservationsViewSet(viewsets.ModelViewSet):
    """Вьюсет  для обработки бронирования"""

    queryset = Reservation.objects.all()
    serializer_class = ReservationsEditSerializer

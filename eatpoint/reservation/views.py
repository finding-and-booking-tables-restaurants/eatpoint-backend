from rest_framework import viewsets 
from .models import Restaurant_reservations
from .serializers import ReservationsSerializer
# Create your views here.

class ReservationsViewSet(viewsets.ModelViewSet):
    """Вьюсет  для обработки бронирования"""
    queryset = Restaurant_reservations.objects.all()
    serializer_class = ReservationsSerializer
    

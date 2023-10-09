from rest_framework import serializers
from reservation.models import EstablishmentReserv
from establishments.models import TableEstablishment
from api.serializers.user import UserSerializer
from api.serializers.establishments import EstablishmentSerializer

class TableEstablishmentSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = TableEstablishment
        fields = [
            'id',
            'name',
            'description',
            'slug',
        ]



class ReservationsSerializer(serializers.ModelSerializer):

    table = serializers.StringRelatedField(many=False, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    establishment = serializers.StringRelatedField(read_only = True)  


    class Meta:
        fields = (
            'id', 
            'user', 
            'email', 
            'telephone', 
            'establishment', 
            'table', 
            'Number_of_guests',
            'date_reservation',
            'start_time_reservation',
            'end_time_reservation',
            'comment',
            'reminder_one_day',
            'reminder_three_hours',
            'reminder_half_on_hour',
            )
        model = EstablishmentReserv


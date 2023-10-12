from rest_framework import serializers
from reservation.models import EstablishmentReserv
from establishments.models import ZoneEstablishment
from api.serializers.users import UserSerializer
from api.serializers.establishments import EstablishmentSerializer

class ZoneEstablishmentSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = ZoneEstablishment
        fields = [
            'id',
            'establishment',
            'zone',
            'seats',
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
            'zone', 
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


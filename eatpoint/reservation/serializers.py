from rest_framework import serializers
from .models import Restaurant_reservations


class ReservationsSerializer(serializers.ModelSerializer):
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
            'event',
            )
        model = Restaurant_reservations
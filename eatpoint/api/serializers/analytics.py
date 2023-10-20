from rest_framework import serializers
from django.utils.timezone import now


class AnalyticsStaticSerializer(serializers.Serializer):
    daily_reservation = serializers.IntegerField(
        help_text="Бронирования за день",
    )
    weekly_reservation = serializers.IntegerField(
        help_text="Бронирования за неделю",
    )
    yearly_reservation = serializers.IntegerField(
        help_text="Бронирования за год",
    )
    total_reservation = serializers.IntegerField(
        help_text="Бронирования за все время",
    )

    def to_representation(self, instance):
        return {
            "total_reservation": instance["total_reservation"],
            "daily_reservation": instance["daily_reservation"],
            "weekly_reservation": instance["weekly_reservation"],
            "yearly_reservation": instance["yearly_reservation"],
        }


class AnalyticsDynamicSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M",
        default="1999-01-01 10:00",
        write_only=True,
        help_text="Начало отслеживания",
    )
    end_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M",
        default=now(),
        write_only=True,
        help_text="Конец отслеживания",
    )
    total_reservation = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        return {
            "total_reservation": instance["total_reservation"],
        }

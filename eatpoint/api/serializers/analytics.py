from rest_framework import serializers

from django.utils.timezone import now


class AnalyticsStaticSerializer(serializers.Serializer):
    """
    Сериализатор для статической аналитики бронирований.

    Предоставляет статистические данные о бронированиях за различные периоды времени.
    """

    daily_reservation = serializers.IntegerField(
        help_text="Бронирования за день",
    )
    weekly_reservation = serializers.IntegerField(
        help_text="Бронирования за неделю",
    )
    monthly_reservation = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="Бронирования по месяцам",
    )
    daily_reservations_last_week = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="Бронирования по дням",
    )
    yearly_reservation = serializers.IntegerField(
        help_text="Бронирования за год",
    )
    total_reservation = serializers.IntegerField(
        help_text="Бронирования за все время",
    )

    def to_representation(self, instance):
        """
        Преобразует объект сериализатора в словарь с данными аналитики.

        Args:
            instance: Экземпляр сериализатора.

        Returns:
            dict: Словарь с данными аналитики.
        """
        return {
            "total_reservation": instance["total_reservation"],
            "daily_reservation": instance["daily_reservation"],
            "weekly_reservation": instance["weekly_reservation"],
            "daily_reservations_last_week": instance[
                "daily_reservations_last_week"
            ],
            "monthly_reservation": instance["monthly_reservation"],
            "yearly_reservation": instance["yearly_reservation"],
        }


class AnalyticsDynamicSerializer(serializers.Serializer):
    """Аналитика зы выбранные период"""

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
    daily_reservations_last_week = serializers.ListField(
        child=serializers.DictField(), read_only=True
    )
    daily_reservations = serializers.ListField(
        child=serializers.DictField(), read_only=True
    )
    monthly_reservations = serializers.ListField(
        child=serializers.DictField(), read_only=True
    )

    def to_representation(self, instance):
        representation = {
            "total_reservation": instance.get("total_reservation"),
            "daily_reservations_last_week": instance.get(
                "daily_reservations_last_week"
            ),
            "daily_reservations": instance.get("daily_reservations"),
            "monthly_reservations": instance.get("monthly_reservations"),
        }
        return representation

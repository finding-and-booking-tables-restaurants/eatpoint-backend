from rest_framework import serializers

from django.utils.timezone import now


class AnalyticsStaticSerializer(serializers.Serializer):
    """
    Сериализатор для статической аналитики бронирований.

    Предоставляет статистические данные о бронированиях за различные периоды времени.
    """

    total_reservation = serializers.IntegerField(
        help_text="Бронирования за все время",
    )
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
    yearly_reservation = serializers.IntegerField(
        help_text="Бронирования за год",
    )
    daily_reservations_by_day = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="Бронирования по дням",
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
            "monthly_reservation": instance["monthly_reservation"],
            "yearly_reservation": instance["yearly_reservation"],
            "daily_reservations_by_day": instance["daily_reservations_by_day"],
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

    total_reservation = serializers.IntegerField(
        help_text="Бронирования за все время", read_only=True
    )
    daily_reservations_by_day = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="Бронирования по дням",
        read_only=True,
    )
    monthly_reservations_by_month = serializers.DictField(
        read_only=True,
        child=serializers.IntegerField(),
        help_text="Бронирования по месяцам",
    )
    yearly_reservation = serializers.IntegerField(
        read_only=True,
        help_text="Бронирования за год",
    )

    def to_representation(self, instance):
        representation = {
            "total_reservation": instance.get("total_reservation"),
            "daily_reservations_by_day": instance.get(
                "daily_reservations_by_day"
            ),
            "monthly_reservations_by_month": instance.get(
                "monthly_reservations_by_month"
            ),
            "yearly_reservation": instance.get("yearly_reservation"),
        }
        return representation

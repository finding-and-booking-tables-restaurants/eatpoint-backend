from rest_framework import serializers
from django.db.models import Count

from django.utils.timezone import now

from establishments.models import Establishment
from reservation.models import Reservation


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
            "yearly_reservation": instance["yearly_reservation"],
        }


class AnalyticsDynamicSerializer(serializers.Serializer):
    """
    Сериализатор для аналитики в выбранном временном периоде.

    Предоставляет возможность получения аналитических данных о бронированиях
    для указанного заведения в указанном временном диапазоне.
    """

    start_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M",
        default="1999-01-01 10:00",
        write_only=True,
        help_text="Начало отслеживания",
    )
    end_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M",
        write_only=True,
        help_text="Конец отслеживания",
    )
    total_reservation = serializers.IntegerField(read_only=True)

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
        }

    def get_reservation_analytics(
        self, start_date, end_date, establishment_id
    ):
        """
        Получает данные аналитики по бронированиям для указанного заведения в указанном временном диапазоне.

        Args:
            start_date (datetime.datetime): Начальная дата отслеживания бронирований.
            end_date (datetime.datetime): Конечная дата отслеживания бронирований.
            establishment_id (int): ID заведения для получения аналитики.

        Returns:
            int: Общее количество бронирований за указанный период времени.

        Raises:
            serializers.ValidationError: Если указанное заведение не существует.
        """
        end_date = end_date or now()

        try:
            establishment = Establishment.objects.get(id=establishment_id)
        except Establishment.DoesNotExist:
            raise serializers.ValidationError(
                "Указанное заведение не существует"
            )

        reservations = (
            Reservation.objects.filter(
                establishment=establishment,
                date_reservation__range=(start_date, end_date),
            )
            .values("date_reservation__date")
            .annotate(reservation_count=Count("id"))
        )

        analytics = {
            res["date_reservation__date"]: res["reservation_count"]
            for res in reservations
        }

        return sum(analytics.values())

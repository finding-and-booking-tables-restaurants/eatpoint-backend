from django_filters.rest_framework import FilterSet, filters

from reservation.models import Slot


class SlotsFilter(FilterSet):
    """Фильтры слотов"""

    zone = filters.CharFilter(field_name="zone__zone")
    date = filters.DateFilter(field_name="date")
    seats = filters.NumberFilter(field_name="seats")

    class Meta:
        model = Slot
        fields = ["date", "seats", "zone"]

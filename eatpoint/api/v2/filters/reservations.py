from django_filters.rest_framework import FilterSet, filters

from reservation.models import Slot


class SlotsFilter(FilterSet):
    """Фильтры слотов"""

    zone = filters.CharFilter(field_name="zone__zone")

    class Meta:
        model = Slot
        fields = ["date", "seats", "zone"]

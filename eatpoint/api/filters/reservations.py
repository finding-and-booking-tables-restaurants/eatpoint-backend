from django_filters.rest_framework import FilterSet, filters

from reservation.models import Slot


class SlotsFilter(FilterSet):
    """Фильтры слотов"""

    seats = filters.ModelMultipleChoiceFilter(
        field_name="seats",
        queryset=Slot.objects.all(),
        to_field_name="seats",
    )

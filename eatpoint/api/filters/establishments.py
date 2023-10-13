from django_filters.rest_framework import filters, FilterSet

from core.choices import CHECK_CHOICES
from establishments.models import Establishment, Service, TypeEst, Kitchen


class EstablishmentFilter(FilterSet):
    kitchens = filters.ModelMultipleChoiceFilter(
        field_name="kitchens__slug",
        queryset=Kitchen.objects.all(),
        to_field_name="slug",
    )
    types = filters.ModelMultipleChoiceFilter(
        field_name="types__slug",
        queryset=TypeEst.objects.all(),
        to_field_name="slug",
    )
    services = filters.ModelMultipleChoiceFilter(
        field_name="services__slug",
        queryset=Service.objects.all(),
        to_field_name="slug",
    )
    average_check = filters.ChoiceFilter(
        choices=CHECK_CHOICES,
    )

    class Meta:
        model = Establishment
        fields = [
            "services",
            "kitchens",
            "types",
            "average_check",
        ]

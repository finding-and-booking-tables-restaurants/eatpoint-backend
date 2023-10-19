from django_filters.rest_framework import filters, FilterSet
from rest_framework.filters import SearchFilter

from core.choices import CHECK_CHOICES
from establishments.models import (
    Establishment,
    Service,
    TypeEst,
    Kitchen,
    City,
)


class EstablishmentFilter(FilterSet):
    """Фильтры заведения"""

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
        field_name="services__name",
        queryset=Service.objects.all(),
        to_field_name="slug",
    )
    average_check = filters.ChoiceFilter(
        choices=CHECK_CHOICES,
    )
    cities = filters.ModelChoiceFilter(
        field_name="cities__name",
        queryset=City.objects.all(),
        to_field_name="slug",
    )
    is_favorited = filters.BooleanFilter(method="filters_favorited")

    class Meta:
        model = Establishment
        fields = [
            "services",
            "kitchens",
            "types",
            "average_check",
            "cities",
            "is_favorited",
        ]

    def filters_favorited(self, queryset, name, value):
        """Возвращает только избранное пользователя"""
        if not self.request.user.is_authenticated:
            return Establishment.objects.none()
        elif value:
            return queryset.filter(favorite__user=self.request.user)
        return Establishment.objects.all()


class CityFilter(SearchFilter):
    """Поиск по городу"""

    search_param = "name"

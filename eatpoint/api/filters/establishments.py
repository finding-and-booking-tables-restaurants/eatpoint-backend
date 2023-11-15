from django_filters.rest_framework import filters, FilterSet
from rest_framework.filters import SearchFilter
from rest_framework.validators import ValidationError

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
    location = filters.CharFilter(method="filter_location")

    class Meta:
        model = Establishment
        fields = [
            "services",
            "kitchens",
            "types",
            "average_check",
            "cities",
            "is_favorited",
            "location",
        ]

    def filters_favorited(self, queryset, name, value):
        """Возвращает только избранное пользователя"""
        if not self.request.user.is_authenticated:
            return Establishment.objects.none()
        elif value:
            return queryset.filter(favorite__user=self.request.user)
        return Establishment.objects.all()

    def filter_location(self, queryset, name, value):
        try:
            lat, lon = map(float, value.split(","))
            return queryset.filter(
                latitude__range=(lat - 0.05, lat + 0.05),
                longitude__range=(lon - 0.05, lon + 0.05),
            )
        except ValueError:
            raise ValidationError(
                {
                    "location": "Введите корректную позицию в формате широта,долгота"
                }
            )


class CityFilter(SearchFilter):
    """Поиск по городу"""

    search_param = "name"

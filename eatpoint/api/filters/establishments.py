from rest_framework import filters


class EstablishmentFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        establishment_kitchens = request.query_params.getlist("kitchens")
        review_queryset = queryset
        if establishment_kitchens:
            regular_tags = "|".join(establishment_kitchens)
            review_queryset = review_queryset.filter(
                kitchens__slug__regex=regular_tags
            )
        return review_queryset.distinct()


class TypeEstFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        establishment_types = request.query_params.getlist("types")
        review_queryset = queryset
        if establishment_types:
            regular_tags = "|".join(establishment_types)
            review_queryset = review_queryset.filter(
                types__slug__regex=regular_tags
            )
        return review_queryset.distinct()


class ServicesEstFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        establishment_services = request.query_params.getlist("services")
        review_queryset = queryset
        if establishment_services:
            regular_tags = "|".join(establishment_services)
            review_queryset = review_queryset.filter(
                services__slug__regex=regular_tags
            )
        return review_queryset.distinct()

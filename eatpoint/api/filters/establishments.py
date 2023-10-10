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

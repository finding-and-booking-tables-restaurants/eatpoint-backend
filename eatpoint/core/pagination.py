from rest_framework.pagination import PageNumberPagination

from core.constants import PAGE_SIZE, SLOTS_PAGE_SIZE


class LargeResultsSetPagination(PageNumberPagination):
    """Пагинация"""

    page_size = PAGE_SIZE
    page_size_query_param = "page_size"


class SlotsPagination(PageNumberPagination):
    """Пагинация для слотов"""

    page_size = SLOTS_PAGE_SIZE
    page_size_query_param = "page_size"

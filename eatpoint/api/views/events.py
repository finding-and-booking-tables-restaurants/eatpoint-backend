from rest_framework import viewsets

from api.serializers import events as ser
from events.crud import list_events, list_event_types


class TypeEventViewset(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки Типов событий."""

    queryset = list_event_types()

    def get_serializer_class(self):
        if self.action == "list":
            return ser.ListTypeEventSerializer
        return ser.RetrieveTypeEventSerializer


class EventViewset(viewsets.ModelViewSet):
    """Вьюсет для обработки Событий."""

    queryset = list_events()

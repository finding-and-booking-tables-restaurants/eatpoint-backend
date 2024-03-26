from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)

from api.v2.serializers.reservations import (
    UpdateReservationActionSerializer,
    ReservationsUpdateUserSerializer,
)


reservations_edit_schema = {
    "methods": ["POST"],
    "description": "Клиент",
}
reservations_edit_schema_view = {
    "create": extend_schema(
        summary="Добавить бронирование",
        parameters=[
            OpenApiParameter(
                name="establishment_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
        examples=[
            OpenApiExample(
                name="Создание брони - зарегистрированный пользователь",
                request_only=True,
                value={
                    "slots": [1, 2],
                    "comment": "комментарий",
                    "reminder_one_day": True,
                    "reminder_three_hours": True,
                    "reminder_half_on_hour": True,
                },
            ),
            OpenApiExample(
                name="Создание брони - зарегистрированный пользователь",
                response_only=True,
                value={
                    "id": 1,
                    "date_reservation": "2020-01-01",
                    "start_time_reservation": "10:00",
                    "establishment": 1,
                    "slots": [1, 2],
                    "comment": "комментарий",
                    "reminder_one_day": True,
                    "reminder_three_hours": True,
                    "reminder_half_on_hour": True,
                },
            ),
            OpenApiExample(
                name="Создание брони - не зарегистрированный пользователь",
                request_only=True,
                value={
                    "slots": [1, 2],
                    "comment": "комментарий",
                    "reminder_one_day": True,
                    "reminder_three_hours": True,
                    "reminder_half_on_hour": True,
                    "telephone": "79876543210",
                    "email": "anonim@example.com",
                    "first_name": "Анон",
                    "last_name": "Анонимов",
                },
            ),
            OpenApiExample(
                name="Создание брони - не зарегистрированный пользователь",
                response_only=True,
                value={
                    "id": 1,
                    "slots": [1, 2],
                    "first_name": "Анон",
                    "last_name": "Анонимов",
                    "email": "anonim@example.com",
                    "telephone": "79876543210",
                    "comment": "комментарий",
                    "date_reservation": "2020-01-01",
                    "start_time_reservation": "10:00",
                    "establishment": 1,
                    "reminder_one_day": True,
                    "reminder_three_hours": True,
                    "reminder_half_on_hour": True,
                },
            ),
        ],
    ),
}

ReservationsUserListViewSet_schema = {
    "methods": ["GET", "DELETE", "PATCH"],
    "description": "Клиент/ресторатор",
}
ReservationsUserListViewSet_schema_view = {
    "list": extend_schema(
        summary="Получить список бронирований",
    ),
    "retrieve": extend_schema(
        summary="Детальная информация о бронировании заведения",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
    "destroy": extend_schema(
        summary="Удалить бронирование",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
    "partial_update": extend_schema(
        summary="Изменить данные бронирования",
        request=ReservationsUpdateUserSerializer,
        responses={200: ReservationsUpdateUserSerializer},
        parameters=[
            OpenApiParameter(
                name="establishment_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            ),
        ],
        examples=[
            OpenApiExample(
                "Example for deleted",
                description="Отменить бронирование",
                value={
                    "action": "is_deleted",
                },
            ),
        ],
    ),
}

ReservationsRestorateurListViewSet_schema = {
    "methods": ["GET", "DELETE", "PATCH"],
    "description": "Ресторатор",
}
ReservationsRestorateurListViewSet_schema_view = {
    "list": extend_schema(
        summary="Получить список бронирований",
    ),
    "retrieve": extend_schema(
        summary="Детальная информация о бронировании заведения",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
    "destroy": extend_schema(
        summary="Удалить бронирование",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
    "partial_update": extend_schema(
        summary="Принять бронирование или отметить бронирование как выполненное",
        request=UpdateReservationActionSerializer,
        examples=[
            OpenApiExample(
                "Example for accepting",
                description="Принять бронирование",
                value={
                    "action": "is_accepted",
                },
            ),
            OpenApiExample(
                "Example for visited",
                description="Отметить бронирование как выполненное",
                value={
                    "action": "is_visited",
                },
            ),
            OpenApiExample(
                "Example for deleted",
                description="Отменить бронирование",
                value={
                    "action": "is_deleted",
                },
            ),
        ],
    ),
}

ReservationsHistoryListViewSet_schema = {
    "methods": ["GET"],
    "description": "Клиент/ресторатор",
}
ReservationsHistoryListViewSet_schema_view = {
    "list": extend_schema(
        summary="Получить список истории броней заведения",
    ),
    "retrieve": extend_schema(
        summary="Детальная информация о броне заведения",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
            )
        ],
    ),
}

AvailableSlotsViewSet_schema = {
    "methods": ["GET"],
    "description": "Все пользователи",
}
AvailableSlotsViewSet_schema_view = {
    "list": extend_schema(
        summary="Получить список слотов к заведению с id",
    ),
    "retrieve": extend_schema(
        summary="Детальная информация о слоте",
    ),
}

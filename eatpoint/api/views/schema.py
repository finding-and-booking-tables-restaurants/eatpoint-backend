from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

reservations_edit_schema = {
    "tags": ["Бронирование"],
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
    ),
}

ReservationsUserListViewSet_schema = {
    "tags": ["Мои бронирования"],
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
    ),
}

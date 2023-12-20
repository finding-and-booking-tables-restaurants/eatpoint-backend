from drf_spectacular.utils import extend_schema


business_events_schema = {
    "list": extend_schema(
        summary="Получить список событий",
        description="Ресторатор",
    ),
    "destroy": extend_schema(
        summary="Удалить событие",
        description="Ресторатор",
    ),
    "create": extend_schema(
        summary="Создать событие",
        description="Ресторатор",
    ),
    "retrieve": extend_schema(
        summary="Одно событий",
        description="Ресторатор",
    ),
    "partial_update": extend_schema(
        summary="Редактировать событие",
        description="Ресторатор",
    ),
}

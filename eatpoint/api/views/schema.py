from drf_spectacular.utils import extend_schema, OpenApiExample

from ..serializers.events import (
    CreateEditEventSerializer,
    RetrieveEventSrializer,
)


event_short_response = {
    "id": 1,
    "name": "Новый Год",
    "establishment": {
        "id": 1,
        "name": "Лучшее место",
        "address": "Невский пр, 60",
        "telephone": "+79991234567",
    },
    "image": "https://eatpoint.site/media/.../123.png",
    "date_start": "30.12.2023 20:22",
    "price": 2500,
    "type_event": [{"id": 1, "name": "Вечеринка"}],
}

event_full_response = {
    "id": 1,
    "name": "Новый Год",
    "establishment": {
        "id": 1,
        "name": "Лучшее место",
        "address": "Невский пр, 60",
        "telephone": "+79991234567",
    },
    "image": "https://eatpoint.site/media/.../123.png",
    "date_start": "31.12.2023 20:00",
    "price": 2500,
    "type_event": [{"id": 1, "name": "Вечеринка"}],
    "description": "Тут много слов о событии",
    "date_end": "01.01.2024 10:00",
    "photos": [{"id": 1, "image": "https://eatpoint.site/media/.../123.png"}],
}

event_request = {
    "name": "Новый Год",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA",
    "date_start": "31.12.2023 20:00",
    "price": 2500,
    "type_event": [1],
    "description": "Тут много слов о событии",
    "date_end": "01.01.2024 10:00",
}

business_events_schema = {
    "list": extend_schema(
        summary="Получить список событий",
        description="Ресторатор",
        examples=[
            OpenApiExample(
                name="Список событий",
                value=[event_short_response],
            )
        ],
    ),
    "destroy": extend_schema(
        summary="Удалить событие",
        description="Ресторатор",
    ),
    "create": extend_schema(
        summary="Создать событие",
        description="Ресторатор",
        request=CreateEditEventSerializer,
        responses={201: RetrieveEventSrializer},
        examples=[
            OpenApiExample(
                name="Создание события - запрос",
                value=event_request,
                request_only=True,
            ),
            OpenApiExample(
                name="Создание события - ответ",
                value=event_full_response,
                response_only=True,
            ),
        ],
    ),
    "retrieve": extend_schema(
        summary="Просмотр одного события",
        description="Ресторатор",
        examples=[
            OpenApiExample(
                name="Детали по событию",
                value=event_full_response,
            )
        ],
    ),
    "partial_update": extend_schema(
        summary="Редактировать событие",
        description="Ресторатор",
        request=CreateEditEventSerializer,
        responses={201: RetrieveEventSrializer},
        examples=[
            OpenApiExample(
                name="Изменение события - запрос",
                value=event_request,
                request_only=True,
            ),
            OpenApiExample(
                name="Изменение события - ответ",
                value=event_full_response,
                response_only=True,
            ),
        ],
    ),
}

users_events_schema = {
    "list": extend_schema(
        summary="Получить список событий",
        description="Любой пользователь",
        examples=[
            OpenApiExample(
                name="Список событий",
                value=[event_short_response],
            )
        ],
    ),
    "retrieve": extend_schema(
        summary="Просмотр одного события",
        description="Любой пользователь",
        examples=[
            OpenApiExample(
                name="Детали по событию",
                value=event_full_response,
            )
        ],
    ),
}


events_photo_schema = {
    "list": extend_schema(
        summary="Получить список фото события",
        description="Ресторатор",
    ),
    "destroy": extend_schema(
        summary="Удалить фото события",
        description="Ресторатор",
    ),
    "create": extend_schema(
        summary="Добавить фото события",
        description="Ресторатор",
    ),
    "retrieve": extend_schema(
        summary="Просмотр одного фото события",
        description="Ресторатор",
    ),
}

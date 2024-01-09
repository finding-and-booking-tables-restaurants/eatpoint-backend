from drf_spectacular.utils import extend_schema, OpenApiExample

from ..serializers.events import (
    CreateEventSerializer,
    RetrieveEventSrializer,
    UpdateEventSerializer,
)


event_request = {
    "name": "Новый Год",
    "cover_image": 1,
    "date_start": "31.12.2023 20:00",
    "price": 2500,
    "type_event": [1, 2],
    "photos": [6, 7],
    "description": "Тут много слов о событии",
    "recur_settings": {"recurrence": 1, "date_end": "2024-01-07"},
}

event_short_response = {
    "id": 79,
    "name": "Новогодняя елка",
    "establishment": {
        "id": 1,
        "name": "Пиццерия",
        "address": "ул. Мирная, 14",
        "telephone": "+79998998878",
    },
    "cover_image": {
        "id": 8,
        "image": "http://eatpoint.site/media/establishment/../48413f.png",
    },
    "date_start": "01.01.2024 16:00",
    "price": 3000,
    "type_event": [],
}

event_full_response = {
    "id": 83,
    "name": "Новогодняя елка",
    "establishment": {
        "id": 1,
        "name": "Пиццерия",
        "address": "ул. Мирная, 14",
        "telephone": "+79998998878",
    },
    "cover_image": {
        "id": 8,
        "image": "http://eatpoint.site/media/establishment/../8413f.png",
    },
    "date_start": "05.01.2024 16:00",
    "price": 3500,
    "type_event": [{"id": 1, "name": "Вечеринка"}],
    "description": "",
    "photos": [
        {
            "id": 6,
            "image": "http://eatpoint.site/media/establishment/../06cc2.png",
        },
        {
            "id": 7,
            "image": "http://eatpoint.site/media/establishment/../77921.png",
        },
    ],
    "recur_settings": {"recurrence": "Ежедневно", "date_end": "2024-01-07"},
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
        request=CreateEventSerializer,
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
        request=UpdateEventSerializer,
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
    "update_seria": extend_schema(
        summary="Редактировать серию событий, начиная с указанного",
        description="Ресторатор",
        request=CreateEventSerializer,
        responses={201: RetrieveEventSrializer},
        examples=[
            OpenApiExample(
                name="Изменение серии событий - запрос",
                value=event_request,
                request_only=True,
            ),
            OpenApiExample(
                name="Изменение серии событий - ответ",
                value=event_full_response,
                response_only=True,
            ),
        ],
    ),
    "delete_seria": extend_schema(
        summary="Удалить серию событий, начиная с указанного",
        description="Ресторатор",
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
    "destroy": extend_schema(
        summary="Удалить фото события",
        description="Ресторатор",
    ),
    "create": extend_schema(
        summary="Добавить фото события",
        description="Ресторатор",
    ),
}


events_types_schema = {
    "list": extend_schema(
        summary="Получить список типов событий",
        description="Любой пользователь",
    ),
    "retrieve": extend_schema(
        summary="Просмотр одного типа события события",
        description="Любой пользователь",
    ),
}

recurrencies_schema = {
    "list": extend_schema(
        summary="Получить список Периодов повтора событий",
        description="Любой пользователь",
    ),
    "retrieve": extend_schema(
        summary="Просмотр одного Периода повтора событий ",
        description="Любой пользователь",
    ),
}

from rest_framework.validators import ValidationError
from django.core.exceptions import ValidationError as ValidateModelImage
from django.conf import settings
from rest_framework import serializers


def file_size(value):
    limit = settings.IMAGE_SIZE
    if value.size > limit:
        raise ValidateModelImage(
            "Размер изображения не должен превышать 5 mb."
        )


def validate_count(data):
    for value in data:
        amount = int(value.get("amount"))
        if amount < settings.MIN_AMOUNT:
            raise ValidationError(
                {"amount": "Количество не может быть меньше 1"}
            )
        if amount > settings.MAX_AMOUNT:
            raise ValidationError(
                {"amount": "Количество не может быть меньше 1000"}
            )
    return data


def validate_uniq(fields, validate_field):
    items = []
    for item in fields:
        items.append(item[validate_field])
    if items != list(set(items)):
        raise serializers.ValidationError(
            "Можно добавить не более 1 уникального поля"
        )

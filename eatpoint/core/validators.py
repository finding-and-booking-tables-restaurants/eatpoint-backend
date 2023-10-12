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


def validate_reserv_anonim(user, validated_data):
    if not user.is_authenticated and "first_name" not in validated_data:
        raise ValidationError(
            {"first_name": "Заполните имя или зарегистрируйтесь"}
        )
    if not user.is_authenticated and "last_name" not in validated_data:
        raise ValidationError(
            {"first_name": "Заполните фамилию или зарегистрируйтесь"}
        )
    if not user.is_authenticated and "telephone" not in validated_data:
        raise ValidationError(
            {"first_name": "Заполните номер телефона или зарегистрируйтесь"}
        )
    if not user.is_authenticated and "email" not in validated_data:
        raise ValidationError(
            {"first_name": "Заполните email телефона или зарегистрируйтесь"}
        )

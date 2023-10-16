from django.core.validators import RegexValidator
from rest_framework.validators import ValidationError
from django.conf import settings
from rest_framework import serializers

from core.constants import IMAGE_SIZE


string_validator = RegexValidator(
    r"^[a-zA-Zа-яА-Я]+$", "Имя и Фамилия должны содержать только буквы"
)


def file_size(value):
    """Валидатор: размер файла"""
    limit = IMAGE_SIZE
    if value.size > limit:
        raise ValidationError("Размер изображения не должен превышать 5 mb.")


def validate_count(data):
    """Валидатор: макс. и мин. количество"""
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
    """Валидатор: уникальное поле"""
    items = []
    for item in fields:
        items.append(item[validate_field])
    if items != list(set(items)):
        raise serializers.ValidationError(
            "Можно добавить не более 1 уникального поля"
        )


def validate_reserv_anonim(user, validated_data):
    """Валидатор: анонимный юзер и обязательные поля"""
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


def validate_time(validated_data):
    """Валидатор: время бронирования"""
    if validated_data.get("start_time_reservation") >= validated_data.get(
        "end_time_reservation"
    ):
        raise ValidationError(
            {"time": "Время начала бронирования не может быть больше конца"}
        )

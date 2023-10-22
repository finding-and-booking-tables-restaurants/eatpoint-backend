from django.core.validators import RegexValidator
from rest_framework.validators import ValidationError
import locale

from core.constants import IMAGE_SIZE, IMAGE_COUNT
from establishments.models import WorkEstablishment, ZoneEstablishment

string_validator = RegexValidator(
    r"^[a-zA-Zа-яА-Я]{2,30}$",
    "Имя и Фамилия должны содержать только "
    "рус и лат буквы длиной от 2 до 30 символов",
)


def file_size(value):
    """Валидатор: размер файла"""
    limit = IMAGE_SIZE
    if value.size > limit:
        raise ValidationError(
            {"image": "Размер изображения не должен превышать 1 mb."},
        )


def validate_count(images):
    """Валидатор: макс. количество изображений"""
    if len(images) > IMAGE_COUNT:
        raise ValidationError(
            {"images": "Можно загрузить не более 10 изображений."},
        )
    return images


def validate_reserv_anonim(user, validated_data):
    """Валидатор: анонимный юзер и обязательные поля"""
    if not user.is_authenticated and "first_name" not in validated_data:
        raise ValidationError(
            {"first_name": "Заполните имя или зарегистрируйтесь"}
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


def validate_reservation_time_zone(data, establishment):
    """Проверяет время работы заведение и введенное время бронирования, а также зону"""
    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    day_of_week = data.get("date_reservation").strftime("%A").lower()
    # establishment = data.get('establishment')
    zone = data.get("zone")
    working_hours = WorkEstablishment.objects.filter(
        establishment=establishment,
        day=day_of_week,
        day_off=False,
    )
    if not working_hours:
        raise ValidationError("Заведение не работает в указанный день недели")

    if not ZoneEstablishment.objects.filter(
        establishment=establishment, zone=zone
    ):
        raise ValidationError(
            "Выбранная зона не принадлежит к указанному заведению."
        )

    res_start = data.get("start_time_reservation")
    working_hours_est = WorkEstablishment.objects.get(
        establishment=establishment, day=day_of_week
    )
    start = working_hours_est.start
    end = working_hours_est.end

    if not (start <= res_start <= end):
        raise ValidationError(
            "Бронирование возможно только в часы работы заведения"
        )

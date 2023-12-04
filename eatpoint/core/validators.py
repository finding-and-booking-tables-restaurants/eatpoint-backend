from django.core.validators import RegexValidator
from rest_framework.validators import ValidationError
import locale
from datetime import datetime

from core.constants import IMAGE_SIZE, IMAGE_COUNT
from establishments.models import WorkEstablishment, ZoneEstablishment
from reservation.models import Availability

string_validator = RegexValidator(
    r"^[a-zA-Zа-яА-ЯёЁ]{2,30}$",
    "Имя и Фамилия должны содержать только "
    "рус и лат буквы длиной от 2 до 30 символов",
)


def validate_seats(available_seats, number_guests):
    """Проверка кол-ва мест"""
    if available_seats:
        if number_guests == 0:
            raise ValidationError(
                {"seats": "Количество гостей не может быть равно 0"}
            )
        if available_seats < number_guests:
            raise ValidationError(
                {"seats": "Кол-во персон больше кол-ва мест"}
            )
    else:
        raise ValidationError({"seats": "Мест больше нет"})


def file_size(value):
    """Валидатор: размер файла"""
    limit = IMAGE_SIZE
    if value.size > limit:
        raise ValidationError(
            {"image": "Размер изображения не должен превышать 1 mb."},
        )


def validated_available_seats(zone, date):
    """Проверка свободных мест на день"""
    if not Availability.objects.filter(zone=zone, date=date).exists():
        raise ValidationError(
            {"date": f"Нет информации о свободных местах на {date} в {zone}"},
        )

    available_seats = Availability.objects.filter(zone=zone, date=date).first()
    return available_seats


def validate_count(images):
    """Валидатор: макс. количество изображений"""
    if len(images) > IMAGE_COUNT:
        raise ValidationError(
            {"images": "Можно загрузить не более 10 изображений."},
        )
    return images


def validate_uniq(fields, validate_field):
    """Валидатор: уникальное поле"""
    items = []
    for item in fields:
        items.append(item[validate_field])
    items_set = set(items)
    if len(items) != len(items_set):
        raise ValidationError(
            {"workerd": "Можно добавить не более 1 уникального поля"}
        )


def validate_reserv_anonim(user, validated_data):
    """Валидатор: анонимный юзер и обязательные поля"""
    if not user.is_authenticated:
        if "first_name" not in validated_data:
            raise ValidationError(
                {"first_name": "Заполните имя или зарегистрируйтесь"}
            )
        if "telephone" not in validated_data:
            raise ValidationError(
                {
                    "first_name": "Заполните номер телефона или зарегистрируйтесь"
                }
            )
        if "email" not in validated_data:
            raise ValidationError(
                {
                    "first_name": "Заполните email телефона или зарегистрируйтесь"
                }
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
    date = data.get("date_reservation")
    zone = data.get("zone")
    working_hours = WorkEstablishment.objects.filter(
        establishment=establishment,
        day=day_of_week,
        day_off=False,
    )
    if date < datetime.now().date():
        raise ValidationError(
            {
                "date_reservation": f"Введите корректную дадту. Дата не может быть меньше {datetime.now().date()}"
            },
        )
    if not working_hours:
        raise ValidationError(
            {
                "date_reservation": "Заведение не работает в указанный день недели"
            }
        )

    if not ZoneEstablishment.objects.filter(
        establishment=establishment, zone=zone
    ):
        raise ValidationError(
            {"zone": "Выбранная зона не принадлежит к указанному заведению."}
        )

    res_start = data.get("start_time_reservation")
    working_hours_est = WorkEstablishment.objects.get(
        establishment=establishment, day=day_of_week
    )
    start = working_hours_est.start
    end = working_hours_est.end

    if not (start <= res_start <= end):
        raise ValidationError(
            {
                "start_time_reservation": "Бронирование возможно только в часы работы заведения"
            }
        )

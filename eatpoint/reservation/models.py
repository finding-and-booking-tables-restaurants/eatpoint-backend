from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

from establishments.models import Establishment, ZoneEstablishment

from users.models import User

# Create your models here.
# TIME_CHOICE =


class Reservation(models.Model):
    """Форма бронирования"""

    user = models.ForeignKey(
        User,
        related_name="reservation",
        on_delete=models.CASCADE,
        null=True,
    )
    first_name = models.CharField(
        "First name",
        max_length=150,
    )
    last_name = models.CharField(
        "Last name",
        max_length=150,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
    )
    telephone = PhoneNumberField(null=True, default=None)
    establishment = models.ForeignKey(
        Establishment,
        related_name="reservation",
        verbose_name="Ресторан",
        on_delete=models.CASCADE,
    )
    zone = models.ForeignKey(
        ZoneEstablishment,
        related_name="reservations",
        verbose_name="Выбранная зона в ресторане",
        on_delete=models.CASCADE,
    )
    number_guests = models.IntegerField(
        verbose_name="Количество гостей",
        validators=[
            MinValueValidator(
                1,  # заменить на константы
                message="Количество мест слишком маленькое",
            ),
            MaxValueValidator(
                20,  # заменить на константы
                message="Количество мест слишком большое",
            ),
        ],
    )
    date_reservation = models.DateField(  # к дате резервирования нужно добавить авто добавление времени.
        verbose_name="Дата бронирования",
        auto_now_add=True,
    )
    start_time_reservation = models.TimeField(  # нужно использовать choices, посмотри в моей модели ресторана старт
        # и окончание работы
        verbose_name="Время начала бронирования",
    )
    end_time_reservation = models.TimeField(  # тут тоже самое
        verbose_name="Время окончания бронирования",
    )
    comment = models.CharField(  # проверить pep8
        verbose_name="Пожелания к заказу",
        max_length=200,
        blank=True,
    )
    reminder_one_day = models.BooleanField(  #
        verbose_name="Напоминание о бронировании за 1 день",
        default=False,
    )
    reminder_three_hours = models.BooleanField(
        verbose_name="Напоминание за 3 часа",
        default=False,
    )
    reminder_half_on_hour = models.BooleanField(
        verbose_name="Напоминание за 30 минут",
        default=False,
    )
    status = models.BooleanField(  # скорее не активен и выолнен, а отправлен и принят.
        # Пока так но нужно будет переделать под большее кол-во вариантов: отменен, история и т.д.
        verbose_name="Статус бронирования Активен/Выполнен",  # Активен - True, Выполнен - False
        default=True,
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return self.establishment.name

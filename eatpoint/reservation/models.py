from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

from core.choices import TIME_CHOICES
from core.constants import MIN_SEATS, MAX_SEATS
from establishments.models import Establishment, ZoneEstablishment

from users.models import User


class Reservation(models.Model):
    """Форма бронирования"""

    user = models.ForeignKey(
        User,
        related_name="reservation",
        on_delete=models.CASCADE,
        null=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=True,
        null=True,
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
                MIN_SEATS,
                message="Количество мест слишком маленькое",
            ),
            MaxValueValidator(
                MAX_SEATS,
                message="Количество мест слишком большое",
            ),
        ],
    )
    date_reservation = models.DateField(
        verbose_name="Дата бронирования",
    )
    start_time_reservation = models.CharField(
        verbose_name="Время начала бронирования",
        choices=TIME_CHOICES,
        max_length=145,
    )
    end_time_reservation = models.CharField(
        verbose_name="Время окончания бронирования",
        choices=TIME_CHOICES,
        max_length=145,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        verbose_name="Пожелания к заказу",
        max_length=200,
        blank=True,
    )
    reminder_one_day = models.BooleanField(
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
    status = models.BooleanField(
        verbose_name="Статус бронирования Активен/Выполнен",
        default=True,
    )
    reservation_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-date_reservation"]

    def __str__(self):
        return self.establishment.name


class ReservationHistory(models.Model):
    """История бронирований"""

    user = models.ForeignKey(
        User,
        related_name="reservationhistory",
        on_delete=models.CASCADE,
        null=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
    )
    telephone = PhoneNumberField(null=True, default=None)
    establishment = models.ForeignKey(
        Establishment,
        related_name="reservationhistory",
        verbose_name="Ресторан",
        on_delete=models.CASCADE,
    )
    zone = models.ForeignKey(
        ZoneEstablishment,
        related_name="reservationhistory",
        verbose_name="Выбранная зона в ресторане",
        on_delete=models.CASCADE,
    )
    number_guests = models.IntegerField(
        verbose_name="Количество гостей",
    )
    date_reservation = models.DateField(
        verbose_name="Дата бронирования",
    )
    start_time_reservation = models.CharField(
        verbose_name="Время начала бронирования",
        choices=TIME_CHOICES,
        max_length=145,
    )
    end_time_reservation = models.CharField(
        verbose_name="Время окончания бронирования",
        choices=TIME_CHOICES,
        max_length=145,
        blank=True,
        null=True,
    )
    comment = models.CharField(
        verbose_name="Пожелания к заказу",
        max_length=200,
        blank=True,
    )
    status = models.BooleanField(
        verbose_name="Статус бронирования Активен/Выполнен",
        default=False,
    )
    reservation_date = models.DateTimeField()

    class Meta:
        verbose_name = "Бронирование(история)"
        verbose_name_plural = "Бронирования(истори)"
        ordering = ["-date_reservation"]

    def __str__(self):
        return self.establishment.name

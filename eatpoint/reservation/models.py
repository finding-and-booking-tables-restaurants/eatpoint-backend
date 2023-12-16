from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

from core.choices import TIME_CHOICES
from establishments.models import Establishment, ZoneEstablishment, Table

from users.models import User


class ConfirmationCode(models.Model):
    """Код подтверждения для бронирования анонима"""

    email = models.EmailField(max_length=50)
    code = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)


class Availability(models.Model):
    """Свободные слоты"""

    establishment = models.ForeignKey(
        Establishment,
        verbose_name="Ресторан",
        on_delete=models.CASCADE,
    )
    zone = models.ForeignKey(ZoneEstablishment, on_delete=models.CASCADE)
    date = models.DateField()
    available_seats = models.PositiveIntegerField(
        verbose_name="Количество свободных мест",
        blank=True,
        null=True,
        help_text="Добавляется автоматически",
    )


class Slot(models.Model):
    """Свободные слоты"""

    establishment = models.ForeignKey(
        Establishment,
        verbose_name="Ресторан",
        on_delete=models.CASCADE,
        null=True,
        related_name="slots",
    )
    zone = models.ForeignKey(
        ZoneEstablishment,
        verbose_name="Зона заведения",
        on_delete=models.CASCADE,
        related_name="slots",
    )
    date = models.DateField()
    time = models.CharField(
        max_length=5,
        choices=TIME_CHOICES,
        verbose_name="Время бронирования",
    )
    table = models.ForeignKey(
        Table,
        verbose_name="Свободные столики",
        on_delete=models.CASCADE,
        blank=True,
        related_name="slots",
    )
    seats = models.PositiveIntegerField(
        verbose_name="Количество мест",
    )
    is_active = models.BooleanField(
        verbose_name="Статус слота",
        default=True,
    )

    class Meta:
        verbose_name = "Свободный слот"
        verbose_name_plural = "Свободные слоты"

    def __str__(self):
        return (
            f"заведение: {self.establishment}, зона: {self.zone}, "
            f"{self.date} {self.time}, стол №{self.table.number},"
            f" мест: {self.seats}"
        )


class Reservation(models.Model):
    """Форма бронирования"""

    reservation_date = models.DateTimeField(
        auto_now=True,
    )

    establishment = models.ForeignKey(
        Establishment,
        verbose_name="Ресторан",
        on_delete=models.CASCADE,
        related_name="reservation",
        null=True,
    )

    date_reservation = models.DateField(
        verbose_name="Дата бронирования",
        blank=True,
        null=True,
    )
    start_time_reservation = models.CharField(
        max_length=5,
        choices=TIME_CHOICES,
        verbose_name="Время начала бронирования",
        null=True,
    )

    user = models.ForeignKey(
        User,
        related_name="reservation",
        on_delete=models.CASCADE,
        blank=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        blank=True,
    )
    telephone = PhoneNumberField(null=True, default=None)

    slots = models.ManyToManyField(
        Slot,
        verbose_name="Забронированные слоты",
        related_name="reservations",
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
        verbose_name="Статус бронирования Активен/Принят",
        default=False,
    )
    reservation_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-reservation_date"]

    def clean(self):
        if not self.user and not self.email:
            raise ValidationError("Заполните хотя бы одно поле user или email")

    def __str__(self):
        return (
            f"заведение: {self.slots.all()[0].establishment},"
            f" зона: {self.slots.all()[0].zone},"
            f" {self.slots.all()[0].date} {self.slots.all()[0].time},"
            f" стол №{self.slots.all()[0].table.number},"
            f" мест: {self.slots.all()[0].table.seats}"
        )


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
    reservation_date = models.DateTimeField(
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Бронирование(история)"
        verbose_name_plural = "Бронирования(истори)"
        ordering = ["-date_reservation"]

    def __str__(self):
        return self.establishment.name

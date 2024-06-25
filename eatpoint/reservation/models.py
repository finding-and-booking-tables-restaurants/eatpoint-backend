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
        ordering = ["date", "time"]

    def __str__(self):
        return (
            f"заведение: {self.establishment}, зона: {self.zone}, "
            f"{self.date} {self.time}, стол №{self.table.number},"
            f" мест: {self.seats}"
        )


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


class Reservation(models.Model):
    """Форма бронирования"""

    reservation_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    establishment = models.ForeignKey(
        Establishment,
        verbose_name="Ресторан",
        on_delete=models.CASCADE,
        related_name="reservation",
        null=True,
    )
    date_reservation = models.DateField(
        verbose_name="Дата брони",
        blank=True,
        null=True,
    )
    start_time_reservation = models.CharField(
        max_length=5,
        choices=TIME_CHOICES,
        verbose_name="Время начала брони",
        null=True,
    )
    is_accepted = models.BooleanField(
        verbose_name="Бронь подтверждена",
        default=False,
    )
    is_visited = models.BooleanField(
        verbose_name="Заведение посещено",
        default=False,
    )
    is_deleted = models.BooleanField(
        verbose_name="Бронь отменена",
        default=False,
    )
    user = models.ForeignKey(
        User,
        related_name="reservation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
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
    telephone = PhoneNumberField(blank=True, null=True, default=None)
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

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-reservation_date"]

    def clean(self):
        if not self.user and not self.email:
            raise ValidationError("Заполните хотя бы одно поле user или email")

    def __str__(self):
        establishment_name = (
            self.establishment.name if self.establishment else "не указано"
        )
        if self.slots.exists():
            slot = self.slots.first()
            table_info = (
                f"зона: {slot.zone}, {slot.date} {slot.time}, "
                f"стол № {slot.table.number}, "
                f"мест: {slot.table.seats}"
            )
        else:
            table_info = (
                f"дата брони: {self.date_reservation}, "
                f"время брони: {self.start_time_reservation}, "
                f"клиент: {self.first_name} {self.last_name}"
            )
        return f"заведение: {establishment_name}, {table_info}"


class ReservationHistory(models.Model):
    """История бронирований"""

    reservation_id = models.CharField(
        verbose_name="id брони",
        max_length=200,
        blank=False,
    )

    reservation_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    establishment = models.CharField(
        verbose_name="Ресторан",
        max_length=200,
        blank=True,
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
    is_accepted = models.BooleanField(
        verbose_name="Бронь подтверждена",
        null=True,
    )
    is_visited = models.BooleanField(
        verbose_name="Ресторан посещен",
        null=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        blank=True,
    )
    telephone = PhoneNumberField(null=True, default=None)
    slots = models.TextField(
        verbose_name="Забронированные слоты",
        max_length=1500,
        blank=True,
    )
    comment = models.CharField(
        verbose_name="Пожелания к заказу",
        max_length=200,
        blank=True,
    )
    reminder_one_day = models.BooleanField(
        verbose_name="Напоминание о бронировании за 1 день",
        null=True,
    )
    reminder_three_hours = models.BooleanField(
        verbose_name="Напоминание за 3 часа",
        null=True,
    )
    reminder_half_on_hour = models.BooleanField(
        verbose_name="Напоминание за 30 минут",
        null=True,
    )

    class Meta:
        verbose_name = "Бронирование(архив)"
        verbose_name_plural = "Бронирования(архив)"
        ordering = ["-date_reservation"]

    def __str__(self):
        return self.establishment

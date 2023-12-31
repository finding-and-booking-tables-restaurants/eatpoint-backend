# Generated by Django 4.2.5 on 2023-11-15 13:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("establishments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Availability",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "available_seats",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Добавляется автоматически",
                        null=True,
                        verbose_name="Количество свободных мест",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ConfirmationCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone_number", models.CharField(max_length=15)),
                ("code", models.CharField(max_length=6)),
                ("is_verified", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, verbose_name="Электронная почта"
                    ),
                ),
                (
                    "telephone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default=None, max_length=128, null=True, region=None
                    ),
                ),
                (
                    "number_guests",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                0, message="Количество мест слишком маленькое"
                            ),
                            django.core.validators.MaxValueValidator(
                                100, message="Количество мест слишком большое"
                            ),
                        ],
                        verbose_name="Количество гостей",
                    ),
                ),
                (
                    "date_reservation",
                    models.DateField(verbose_name="Дата бронирования"),
                ),
                (
                    "start_time_reservation",
                    models.CharField(
                        choices=[
                            ("00:00", "00:00"),
                            ("00:30", "00:30"),
                            ("01:00", "01:00"),
                            ("01:30", "01:30"),
                            ("02:00", "02:00"),
                            ("02:30", "02:30"),
                            ("03:00", "03:00"),
                            ("03:30", "03:30"),
                            ("04:00", "04:00"),
                            ("04:30", "04:30"),
                            ("05:00", "05:00"),
                            ("05:30", "05:30"),
                            ("06:00", "06:00"),
                            ("06:30", "06:30"),
                            ("07:00", "07:00"),
                            ("07:30", "07:30"),
                            ("08:00", "08:00"),
                            ("08:30", "08:30"),
                            ("09:00", "09:00"),
                            ("09:30", "09:30"),
                            ("10:00", "10:00"),
                            ("10:30", "10:30"),
                            ("11:00", "11:00"),
                            ("11:30", "11:30"),
                            ("12:00", "12:00"),
                            ("12:30", "12:30"),
                            ("13:00", "13:00"),
                            ("13:30", "13:30"),
                            ("14:00", "14:00"),
                            ("14:30", "14:30"),
                            ("15:00", "15:00"),
                            ("15:30", "15:30"),
                            ("16:00", "16:00"),
                            ("16:30", "16:30"),
                            ("17:00", "17:00"),
                            ("17:30", "17:30"),
                            ("18:00", "18:00"),
                            ("18:30", "18:30"),
                            ("19:00", "19:00"),
                            ("19:30", "19:30"),
                            ("20:00", "20:00"),
                            ("20:30", "20:30"),
                            ("21:00", "21:00"),
                            ("21:30", "21:30"),
                            ("22:00", "22:00"),
                            ("22:30", "22:30"),
                            ("23:00", "23:00"),
                            ("23:30", "23:30"),
                        ],
                        max_length=145,
                        verbose_name="Время начала бронирования",
                    ),
                ),
                (
                    "end_time_reservation",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("00:00", "00:00"),
                            ("00:30", "00:30"),
                            ("01:00", "01:00"),
                            ("01:30", "01:30"),
                            ("02:00", "02:00"),
                            ("02:30", "02:30"),
                            ("03:00", "03:00"),
                            ("03:30", "03:30"),
                            ("04:00", "04:00"),
                            ("04:30", "04:30"),
                            ("05:00", "05:00"),
                            ("05:30", "05:30"),
                            ("06:00", "06:00"),
                            ("06:30", "06:30"),
                            ("07:00", "07:00"),
                            ("07:30", "07:30"),
                            ("08:00", "08:00"),
                            ("08:30", "08:30"),
                            ("09:00", "09:00"),
                            ("09:30", "09:30"),
                            ("10:00", "10:00"),
                            ("10:30", "10:30"),
                            ("11:00", "11:00"),
                            ("11:30", "11:30"),
                            ("12:00", "12:00"),
                            ("12:30", "12:30"),
                            ("13:00", "13:00"),
                            ("13:30", "13:30"),
                            ("14:00", "14:00"),
                            ("14:30", "14:30"),
                            ("15:00", "15:00"),
                            ("15:30", "15:30"),
                            ("16:00", "16:00"),
                            ("16:30", "16:30"),
                            ("17:00", "17:00"),
                            ("17:30", "17:30"),
                            ("18:00", "18:00"),
                            ("18:30", "18:30"),
                            ("19:00", "19:00"),
                            ("19:30", "19:30"),
                            ("20:00", "20:00"),
                            ("20:30", "20:30"),
                            ("21:00", "21:00"),
                            ("21:30", "21:30"),
                            ("22:00", "22:00"),
                            ("22:30", "22:30"),
                            ("23:00", "23:00"),
                            ("23:30", "23:30"),
                        ],
                        max_length=145,
                        null=True,
                        verbose_name="Время окончания бронирования",
                    ),
                ),
                (
                    "comment",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        verbose_name="Пожелания к заказу",
                    ),
                ),
                (
                    "reminder_one_day",
                    models.BooleanField(
                        default=False,
                        verbose_name="Напоминание о бронировании за 1 день",
                    ),
                ),
                (
                    "reminder_three_hours",
                    models.BooleanField(
                        default=False, verbose_name="Напоминание за 3 часа"
                    ),
                ),
                (
                    "reminder_half_on_hour",
                    models.BooleanField(
                        default=False, verbose_name="Напоминание за 30 минут"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=False,
                        verbose_name="Статус бронирования Активен/Принят",
                    ),
                ),
                (
                    "reservation_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
            ],
            options={
                "verbose_name": "Бронирование",
                "verbose_name_plural": "Бронирования",
                "ordering": ["-date_reservation"],
            },
        ),
        migrations.CreateModel(
            name="ReservationHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, verbose_name="Электронная почта"
                    ),
                ),
                (
                    "telephone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default=None, max_length=128, null=True, region=None
                    ),
                ),
                (
                    "number_guests",
                    models.IntegerField(verbose_name="Количество гостей"),
                ),
                (
                    "date_reservation",
                    models.DateField(verbose_name="Дата бронирования"),
                ),
                (
                    "start_time_reservation",
                    models.CharField(
                        choices=[
                            ("00:00", "00:00"),
                            ("00:30", "00:30"),
                            ("01:00", "01:00"),
                            ("01:30", "01:30"),
                            ("02:00", "02:00"),
                            ("02:30", "02:30"),
                            ("03:00", "03:00"),
                            ("03:30", "03:30"),
                            ("04:00", "04:00"),
                            ("04:30", "04:30"),
                            ("05:00", "05:00"),
                            ("05:30", "05:30"),
                            ("06:00", "06:00"),
                            ("06:30", "06:30"),
                            ("07:00", "07:00"),
                            ("07:30", "07:30"),
                            ("08:00", "08:00"),
                            ("08:30", "08:30"),
                            ("09:00", "09:00"),
                            ("09:30", "09:30"),
                            ("10:00", "10:00"),
                            ("10:30", "10:30"),
                            ("11:00", "11:00"),
                            ("11:30", "11:30"),
                            ("12:00", "12:00"),
                            ("12:30", "12:30"),
                            ("13:00", "13:00"),
                            ("13:30", "13:30"),
                            ("14:00", "14:00"),
                            ("14:30", "14:30"),
                            ("15:00", "15:00"),
                            ("15:30", "15:30"),
                            ("16:00", "16:00"),
                            ("16:30", "16:30"),
                            ("17:00", "17:00"),
                            ("17:30", "17:30"),
                            ("18:00", "18:00"),
                            ("18:30", "18:30"),
                            ("19:00", "19:00"),
                            ("19:30", "19:30"),
                            ("20:00", "20:00"),
                            ("20:30", "20:30"),
                            ("21:00", "21:00"),
                            ("21:30", "21:30"),
                            ("22:00", "22:00"),
                            ("22:30", "22:30"),
                            ("23:00", "23:00"),
                            ("23:30", "23:30"),
                        ],
                        max_length=145,
                        verbose_name="Время начала бронирования",
                    ),
                ),
                (
                    "end_time_reservation",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("00:00", "00:00"),
                            ("00:30", "00:30"),
                            ("01:00", "01:00"),
                            ("01:30", "01:30"),
                            ("02:00", "02:00"),
                            ("02:30", "02:30"),
                            ("03:00", "03:00"),
                            ("03:30", "03:30"),
                            ("04:00", "04:00"),
                            ("04:30", "04:30"),
                            ("05:00", "05:00"),
                            ("05:30", "05:30"),
                            ("06:00", "06:00"),
                            ("06:30", "06:30"),
                            ("07:00", "07:00"),
                            ("07:30", "07:30"),
                            ("08:00", "08:00"),
                            ("08:30", "08:30"),
                            ("09:00", "09:00"),
                            ("09:30", "09:30"),
                            ("10:00", "10:00"),
                            ("10:30", "10:30"),
                            ("11:00", "11:00"),
                            ("11:30", "11:30"),
                            ("12:00", "12:00"),
                            ("12:30", "12:30"),
                            ("13:00", "13:00"),
                            ("13:30", "13:30"),
                            ("14:00", "14:00"),
                            ("14:30", "14:30"),
                            ("15:00", "15:00"),
                            ("15:30", "15:30"),
                            ("16:00", "16:00"),
                            ("16:30", "16:30"),
                            ("17:00", "17:00"),
                            ("17:30", "17:30"),
                            ("18:00", "18:00"),
                            ("18:30", "18:30"),
                            ("19:00", "19:00"),
                            ("19:30", "19:30"),
                            ("20:00", "20:00"),
                            ("20:30", "20:30"),
                            ("21:00", "21:00"),
                            ("21:30", "21:30"),
                            ("22:00", "22:00"),
                            ("22:30", "22:30"),
                            ("23:00", "23:00"),
                            ("23:30", "23:30"),
                        ],
                        max_length=145,
                        null=True,
                        verbose_name="Время окончания бронирования",
                    ),
                ),
                (
                    "comment",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        verbose_name="Пожелания к заказу",
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=False,
                        verbose_name="Статус бронирования Активен/Выполнен",
                    ),
                ),
                (
                    "reservation_date",
                    models.DateTimeField(verbose_name="Дата создания"),
                ),
                (
                    "establishment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservationhistory",
                        to="establishments.establishment",
                        verbose_name="Ресторан",
                    ),
                ),
            ],
            options={
                "verbose_name": "Бронирование(история)",
                "verbose_name_plural": "Бронирования(истори)",
                "ordering": ["-date_reservation"],
            },
        ),
    ]

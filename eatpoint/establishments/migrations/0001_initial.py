# Generated by Django 4.2.5 on 2023-11-15 13:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
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
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="Название города"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=200, verbose_name="Ссылка на город"
                    ),
                ),
            ],
            options={
                "verbose_name": "Город",
                "verbose_name_plural": "Города",
            },
        ),
        migrations.CreateModel(
            name="Establishment",
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
                    "name",
                    models.CharField(
                        max_length=150,
                        unique=True,
                        verbose_name="Название заведения",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        max_length=100, verbose_name="Адрес заведения"
                    ),
                ),
                (
                    "average_check",
                    models.CharField(
                        choices=[
                            ("до 1000", "до 1000"),
                            ("1000 - 2000", "1000 - 2000"),
                            ("2000 - 3000", "2000 - 3000"),
                            ("от 3000", "от 3000"),
                        ],
                        max_length=120,
                        verbose_name="Средний чек",
                    ),
                ),
                (
                    "poster",
                    models.ImageField(
                        blank=True,
                        default="",
                        null=True,
                        upload_to="establishment/images/poster",
                        verbose_name="Постер заведения",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Почта"
                    ),
                ),
                (
                    "telephone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128,
                        region=None,
                        unique=True,
                        verbose_name="Номер телефона",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        max_length=1500,
                        null=True,
                        verbose_name="Описание заведения",
                    ),
                ),
                (
                    "is_verified",
                    models.BooleanField(
                        default=False, verbose_name="Верификация заведения"
                    ),
                ),
            ],
            options={
                "verbose_name": "Заведение",
                "verbose_name_plural": "Заведения",
            },
        ),
        migrations.CreateModel(
            name="Event",
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
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="Название события"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        max_length=5000, verbose_name="Описание события"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="establishment/images/event",
                        verbose_name="Постер события",
                    ),
                ),
                (
                    "date_start",
                    models.DateTimeField(verbose_name="Начало события"),
                ),
                (
                    "date_end",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Окончание события"
                    ),
                ),
                (
                    "price",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Цена события"
                    ),
                ),
            ],
            options={
                "verbose_name": "Событие",
                "verbose_name_plural": "События",
            },
        ),
        migrations.CreateModel(
            name="Favorite",
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
            ],
            options={
                "verbose_name": "Избранное",
                "verbose_name_plural": "Избранное",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="ImageEstablishment",
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
                    "name",
                    models.CharField(
                        max_length=100, verbose_name="Описание изображения"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="establishment/images/est_image",
                        verbose_name="Изображение заведения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение заведения",
                "verbose_name_plural": "Изображения заведения",
            },
        ),
        migrations.CreateModel(
            name="Kitchen",
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
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="Название кухни"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        max_length=2000, verbose_name="Описание кухни"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=200,
                        unique=True,
                        verbose_name="Ссылка на кухню",
                    ),
                ),
            ],
            options={
                "verbose_name": "Кухня",
                "verbose_name_plural": "Кухни",
            },
        ),
        migrations.CreateModel(
            name="Review",
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
                    "text",
                    models.TextField(
                        max_length=500, verbose_name="Текст отзыва"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата публикации"
                    ),
                ),
                (
                    "score",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="Допустимые значние 1-5"
                            ),
                            django.core.validators.MaxValueValidator(
                                5, message="Допустимые значние 1-5"
                            ),
                        ]
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Service",
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
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="Название услуги"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        max_length=2000, verbose_name="Описание услуги"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=200,
                        unique=True,
                        verbose_name="Ссылка на услугу",
                    ),
                ),
            ],
            options={
                "verbose_name": "Доп. услуга",
                "verbose_name_plural": "Доп. услуги",
            },
        ),
        migrations.CreateModel(
            name="TypeEst",
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
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="Тип заведения"
                    ),
                ),
                (
                    "description",
                    models.TextField(max_length=2000, verbose_name="Описание"),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=200, unique=True, verbose_name="Ссылка"
                    ),
                ),
            ],
            options={
                "verbose_name": "Тип заведения",
                "verbose_name_plural": "Типы заведения",
            },
        ),
        migrations.CreateModel(
            name="TypeEvents",
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
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="Тип события"
                    ),
                ),
                (
                    "description",
                    models.TextField(max_length=2000, verbose_name="Описание"),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=200, unique=True, verbose_name="Ссылка"
                    ),
                ),
            ],
            options={
                "verbose_name": "Тип события",
                "verbose_name_plural": "Типы события",
            },
        ),
        migrations.CreateModel(
            name="ZoneEstablishment",
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
                    "zone",
                    models.CharField(max_length=150, verbose_name="Зона"),
                ),
                (
                    "seats",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(
                                100, message="Количество мест слишком большое"
                            ),
                            django.core.validators.MinValueValidator(
                                0,
                                message="Количество мест не может быть меньше 1",
                            ),
                        ],
                        verbose_name="Количество мест",
                    ),
                ),
                (
                    "establishment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="zones",
                        to="establishments.establishment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Зона заведения",
                "verbose_name_plural": "Зоны заведения",
            },
        ),
        migrations.CreateModel(
            name="WorkEstablishment",
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
                    "day",
                    models.CharField(
                        choices=[
                            ("понедельник", "понедельник"),
                            ("вторник", "вторник"),
                            ("среда", "среда"),
                            ("четверг", "четверг"),
                            ("пятница", "пятница"),
                            ("суббота", "суббота"),
                            ("воскресенье", "воскресенье"),
                        ],
                        max_length=100,
                        verbose_name="День недели",
                    ),
                ),
                (
                    "day_off",
                    models.BooleanField(
                        default=False, verbose_name="Выходной"
                    ),
                ),
                (
                    "start",
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
                        verbose_name="Начало работы",
                    ),
                ),
                (
                    "end",
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
                        verbose_name="Конец работы",
                    ),
                ),
                (
                    "establishment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="worked",
                        to="establishments.establishment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Время работы",
                "verbose_name_plural": "Время работы",
            },
        ),
        migrations.CreateModel(
            name="SocialEstablishment",
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
                ("name", models.URLField()),
                (
                    "establishment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="socials",
                        to="establishments.establishment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Соц. сеть",
                "verbose_name_plural": "Соц. сети",
            },
        ),
    ]

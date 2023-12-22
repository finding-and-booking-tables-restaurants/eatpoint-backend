from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

from core.choices import DAY_CHOICES, TIME_CHOICES, CHECK_CHOICES
from core.constants import MAX_SEATS, MIN_SEATS
from users.models import User


class Kitchen(models.Model):
    """Кухня"""

    name = models.CharField(
        verbose_name="Название кухни",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание кухни",
        max_length=2000,
    )
    slug = models.SlugField(
        verbose_name="Ссылка на кухню",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Кухня"
        verbose_name_plural = "Кухни"

    def __str__(self):
        return self.name


class TypeEst(models.Model):
    """Тип заведения"""

    name = models.CharField(
        verbose_name="Тип заведения",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание",
        max_length=2000,
    )
    slug = models.SlugField(
        verbose_name="Ссылка",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Тип заведения"
        verbose_name_plural = "Типы заведения"

    def __str__(self):
        return self.name


class Service(models.Model):
    """Доп. услуги"""

    name = models.CharField(
        verbose_name="Название услуги",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание услуги",
        max_length=2000,
    )
    slug = models.SlugField(
        verbose_name="Ссылка на услугу",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Доп. услуга"
        verbose_name_plural = "Доп. услуги"

    def __str__(self):
        return self.name


class City(models.Model):
    """Город"""

    name = models.CharField(
        verbose_name="Название города",
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name="Ссылка на город",
        max_length=200,
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name


class Establishment(models.Model):
    """Заведение"""

    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="establishment",
        verbose_name="Владелец",
    )
    name = models.CharField(
        verbose_name="Название заведения",
        max_length=150,
        unique=True,
    )
    types = models.ManyToManyField(
        TypeEst,
        verbose_name="Тип заведения",
        related_name="establishments",
    )
    cities = models.ForeignKey(
        City,
        verbose_name="Город",
        related_name="establishments",
        on_delete=models.SET_NULL,
        null=True,
    )
    address = models.CharField(
        verbose_name="Адрес заведения",
        max_length=100,
    )
    latitude = models.FloatField(
        verbose_name="Широта",
        max_length=200,
        blank=True,
        null=True,
    )
    longitude = models.FloatField(
        verbose_name="Долгота",
        max_length=200,
        blank=True,
        null=True,
    )
    kitchens = models.ManyToManyField(
        Kitchen,
        verbose_name="Кухня заведения",
        related_name="establishments",
    )
    services = models.ManyToManyField(
        Service,
        verbose_name="Услуга заведения",
        related_name="establishments",
    )
    average_check = models.CharField(
        verbose_name="Средний чек",
        max_length=120,
        choices=CHECK_CHOICES,
    )
    poster = models.ImageField(
        verbose_name="Постер заведения",
        upload_to="establishment/images/poster",
        blank=True,
        null=True,
        default="",
    )
    email = models.EmailField(
        verbose_name="Почта",
        max_length=254,
        unique=True,
    )
    telephone = PhoneNumberField(
        unique=True,
        verbose_name="Номер телефона",
    )
    description = models.TextField(
        verbose_name="Описание заведения",
        max_length=1500,
        blank=True,
        null=True,
    )
    is_verified = models.BooleanField(
        verbose_name="Верификация заведения",
        default=False,
    )

    class Meta:
        verbose_name = "Заведение"
        verbose_name_plural = "Заведения"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SocialEstablishment(models.Model):
    """Соц. сети"""

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        null=True,
        related_name="socials",
    )
    name = models.URLField()

    class Meta:
        verbose_name = "Соц. сеть"
        verbose_name_plural = "Соц. сети"

    def __str__(self):
        return self.name


class WorkEstablishment(models.Model):
    """Время работы"""

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        null=True,
        related_name="worked",
    )
    day = models.CharField(
        verbose_name="День недели",
        max_length=100,
        choices=DAY_CHOICES,
    )
    day_off = models.BooleanField(
        verbose_name="Выходной",
        default=False,
    )
    start = models.CharField(
        verbose_name="Начало работы",
        choices=TIME_CHOICES,
        max_length=145,
        null=True,
        blank=True,
    )
    end = models.CharField(
        verbose_name="Конец работы",
        choices=TIME_CHOICES,
        max_length=145,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Время работы"
        verbose_name_plural = "Время работы"
        constraints = [
            models.UniqueConstraint(
                fields=["day", "establishment"],
                name="unique_work",
                violation_error_message="Можно добавить только 1 день недели",
            ),
        ]

    def clean(self):
        if self.start and self.end is not None:
            if self.start >= self.end:
                raise ValidationError(
                    {
                        "end": "Укажите корректоное время окончания. Оно не может быть меньше времени начала"
                    }
                )

    def __str__(self):
        return self.day


class ImageEstablishment(models.Model):
    """Несколько изображений"""

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        null=True,
        related_name="images",
    )
    name = models.CharField(
        verbose_name="Описание изображения",
        max_length=100,
    )
    image = models.ImageField(
        verbose_name="Изображение заведения",
        upload_to="establishment/images/est_image",
    )

    class Meta:
        verbose_name = "Изображение заведения"
        verbose_name_plural = "Изображения заведения"

    def __str__(self):
        return self.name


class ZoneEstablishment(models.Model):
    """Зоны заведения"""

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        null=True,
        related_name="zones",
    )
    zone = models.CharField(
        verbose_name="Зона",
        max_length=150,
    )
    seats = models.PositiveSmallIntegerField(
        verbose_name="Количество мест",
        validators=[
            MaxValueValidator(
                MAX_SEATS,
                message="Количество мест слишком большое",
            ),
            MinValueValidator(
                MIN_SEATS,
                message="Количество мест не может быть меньше 1",
            ),
        ],
    )

    class Meta:
        verbose_name = "Зона заведения"
        verbose_name_plural = "Зоны заведения"

    def __str__(self):
        return self.zone


class Table(models.Model):
    """Столики"""

    number = models.PositiveSmallIntegerField(
        verbose_name="Номер столика",
    )

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        null=True,
        related_name="tables",
    )
    zone = models.ForeignKey(
        ZoneEstablishment,
        on_delete=models.CASCADE,
        null=True,
        related_name="tables",
    )

    is_active = models.BooleanField(
        verbose_name="Активен",
        default=True,
    )

    is_reserved = models.BooleanField(
        verbose_name="Забронирован",
        default=False,
    )

    seats = models.PositiveSmallIntegerField(
        verbose_name="Количество мест",
        validators=[
            MaxValueValidator(
                MAX_SEATS,
                message=f"Количество мест не может быть больше {MAX_SEATS}",
            ),
            MinValueValidator(
                MIN_SEATS,
                message=f"Количество мест не может быть меньше {MIN_SEATS}",
            ),
        ],
    )

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"

    def __str__(self):
        return f"номер: {self.number}, мест: {self.seats}, зона: {self.zone}"


class Favorite(models.Model):
    """Избранное"""

    user = models.ForeignKey(
        User,
        related_name="favorite",
        on_delete=models.CASCADE,
    )
    establishment = models.ForeignKey(
        Establishment,
        related_name="favorite",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "establishment"], name="uniquefavorit"
            ),
        ]

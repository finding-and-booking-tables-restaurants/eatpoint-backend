from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

from core.choices import DAY_CHOICES, TIME_CHOICES, CHECK_CHOICES
from core.constants import MAX_SEATS, MIN_SEATS
from users.models import User


class Work(models.Model):
    name = models.CharField(
        verbose_name="День недели",
        max_length=100,
        choices=DAY_CHOICES,
    )
    start = models.CharField(
        verbose_name="Начало работы", choices=TIME_CHOICES, max_length=145
    )
    end = models.CharField(
        verbose_name="Конец работы", choices=TIME_CHOICES, max_length=145
    )

    class Meta:
        verbose_name = "Время работы"
        verbose_name_plural = "Время работы"

    def clean(self):
        if self.start >= self.end:
            raise ValidationError(
                {
                    "end": "Укажите корректоное время окончания. Оно не может быть меньше времени начала"
                }
            )

    def __str__(self):
        return self.name


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


class Table(models.Model):
    """Стол"""

    name = models.CharField(
        verbose_name="Название стола",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание стола",
        max_length=2000,
    )
    slug = models.SlugField(
        verbose_name="Ссылка на стол",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"

    def __str__(self):
        return self.name


class Service(models.Model):
    """Доп. услуги"""

    name = models.CharField(
        verbose_name="Название услги",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание услги",
        max_length=2000,
    )
    slug = models.SlugField(
        verbose_name="Ссылка на услгу",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Доп. услуга"
        verbose_name_plural = "Доп. услуги"

    def __str__(self):
        return self.name


class File(models.Model):
    image = models.ImageField(
        verbose_name="Изображение заведения",
        upload_to="establishment/images/est_image",
    )


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
        max_length=200,
        unique=True,
    )
    address = models.CharField(
        verbose_name="Адрес заведения",
        max_length=1000,
    )
    kitchen = models.ManyToManyField(
        Kitchen,
        verbose_name="Кухня заведения",
        related_name="establishments",
    )
    tables = models.ManyToManyField(
        Table,
        through="TableEstablishment",
        verbose_name="Столы заведения",
    )
    file = models.ManyToManyField(
        File,
        through="FileEstablishment",
        verbose_name="Изображения заведения",
    )
    services = models.ManyToManyField(
        Service,
        verbose_name="Услуга заведения",
        related_name="establishments",
    )
    worked = models.ManyToManyField(
        Work,
        through="WorkEstablishment",
        verbose_name="Время работы",
        null=True,
    )
    busy_start = models.CharField(
        verbose_name="Часы загруженности начало",
        choices=TIME_CHOICES,
        max_length=10,
    )
    busy_end = models.CharField(
        verbose_name="Часы загруженности конец",
        choices=TIME_CHOICES,
        max_length=10,
    )
    average_check = models.CharField(
        verbose_name="Средний чек",
        max_length=120,
        choices=CHECK_CHOICES,
    )
    poster = models.ImageField(
        verbose_name="Постер заведения",
        upload_to="establishment/images/poster",
    )
    imagetables = models.ImageField(
        verbose_name="План",
        upload_to="establishment/images/tables",
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=254,
        unique=True,
    )
    telephone = PhoneNumberField()
    social = models.CharField(
        verbose_name="Соц.сеть",
        max_length=1000,
    )
    description = models.TextField(
        verbose_name="Описание заведения",
        max_length=5000,
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

    def clean(self):
        if self.busy_start >= self.busy_end:
            raise ValidationError(
                {
                    "busy_end": "Укажите корректоное время окончания. Оно не может быть меньше времени начала"
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# class Social(models.Model):
#     name


class WorkEstablishment(models.Model):
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    order_dt = models.ForeignKey(
        Work,
        verbose_name="Время работы",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "Время работы"
        verbose_name_plural = "Время работы"

    def __str__(self):
        return self.order_dt.name


class FileEstablishment(models.Model):
    """Несколько изображений"""

    name = models.CharField(
        verbose_name="Описание изображения",
        max_length=100,
    )
    image = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        null=True,
    )
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Изображение заведения"
        verbose_name_plural = "Изображения заведения"

    def __str__(self):
        return f"{self.name}: {self.image}"


class TableEstablishment(models.Model):
    """Столы заведения"""

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.SET_NULL,
        null=True,
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
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
    status = models.BooleanField(
        verbose_name="Статус стола занят/свободен",
        default=False,
    )

    class Meta:
        verbose_name = "Стол заведения"
        verbose_name_plural = "Столы заведения"

    def __str__(self):
        return f"{self.table}-{self.seats} {self.status}"


class Event(models.Model):
    """События"""

    name = models.CharField(
        verbose_name="Название события",
        max_length=200,
    )
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name="event",
    )
    description = models.TextField(
        verbose_name="Описание события",
        max_length=5000,
    )
    image = models.ImageField(
        verbose_name="Постер события",
        upload_to="establishment/images/event",
    )
    date_start = models.DateTimeField(
        verbose_name="Начало события",
    )
    date_end = models.DateTimeField(
        verbose_name="Окончание события",
        blank=True,
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "establishment", "date_start"],
                name="unique_slots",
            ),
        ]

    def __str__(self):
        return f"{self.name}: {self.date_start} - {self.date_end}"


class Review(models.Model):
    """Отзывы"""

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name="review",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="review",
    )
    text = models.TextField(
        verbose_name="Текст отзыва",
        max_length=500,
    )
    created = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["establishment", "author"], name="uniquereview"
            ),
        ]

    def __str__(self):
        return f"{self.author}: {self.text}"

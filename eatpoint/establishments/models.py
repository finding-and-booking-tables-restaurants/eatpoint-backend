from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


# class Day(models.Model):
#     name = models.CharField(
#         verbose_name='День недели',
#         max_length=100,
#     )
#
#     class Meta:
#         verbose_name = 'День недели'
#         verbose_name_plural = 'Дни недели'
#
#     def __str__(self):
#         return self.name


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
    file = models.FileField(
        upload_to="establishment/images/poster",
    )


class Establishment(models.Model):
    """Заведение"""

    name = models.CharField(
        verbose_name="Название заведения",
        max_length=200,
        unique=True,
    )
    address = models.CharField(
        verbose_name="Адрес заведения",
    )
    kitchen = models.ManyToManyField(
        Kitchen,
        verbose_name="Кухня заведения",
        related_name="establishments",
    )
    tables = models.ManyToManyField(  # проверить на манутумени
        Table,
        through="TableEstablishment",
        verbose_name="Стол заведения",
    )
    services = models.ManyToManyField(
        Service,
        verbose_name="Услуга заведения",
        related_name="establishments",
    )
    # worked = models.ManyToManyField(
    #
    # )
    busy = models.DateTimeField(
        verbose_name="Часы загруженности",
    )
    check = models.PositiveIntegerField(
        verbose_name="Средний чек",
    )
    poster = models.ImageField(
        verbose_name="Постер заведения",
        upload_to="establishment/images/poster",
        validators=None,
    )
    file = models.ManyToManyField(
        File,
        verbose_name="Изображения заведения",
        related_name="files",
    )
    imagetables = models.ImageField(
        verbose_name="План",
        upload_to="establishment/images/tables",
        validators=None,
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=254,
        unique=True,
    )
    telephone = models.IntegerField(
        verbose_name="Телефон",
        validators=None,  # сделать валидатор для номера
    )
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


# class Social(models.Model):
#     name


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
                100,  # заменить на константы
                message="Количество мест слишком большое",
            ),
            MinValueValidator(
                1,  # заменить на константы
                message="Количество мест не может быть меньше 1",
            ),
        ],
    )
    status = models.BooleanField(
        verbose_name="Статус стола",
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
        validators=None,
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


# class Worked(models.Model):
#     establishment = models.ForeignKey(
#         Establishment,
#         on_delete=models.SET_NULL,
#         null=True,
#     )
#     day = models.ForeignKey(
#         Day,
#
#     )


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
        validators="Текст отзыва",
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
            models.CheckConstraint(
                check=~models.Q(user=models.F("establishment")),
                name="reviewuniq",
            ),
        ]

    def __str__(self):
        return self.text


# class Reservation(models.Model):
#     user = models.ForeignKey(
#         User,
#         related_name='reservation',
#         on_delete=models.CASCADE,
#     )
#     establishment = models.ForeignKey(
#         Establishment,
#         related_name='reservation',
#     )
#
#     class Meta:
#         verbose_name = 'Бронирование'
#         verbose_name_plural = 'Бронирование'
from django.db import models

from establishments.models import Establishment


class TypeEvent(models.Model):
    """Тип события."""

    name = models.CharField(
        verbose_name="Тип события",
        max_length=200,
    )
    # description = models.TextField(
    #     verbose_name="Описание",
    #     max_length=2000,
    # )
    # slug = models.SlugField(
    #     verbose_name="Ссылка",
    #     max_length=200,
    #     unique=True,
    # )

    class Meta:
        verbose_name = "Тип события"
        verbose_name_plural = "Типы событий"

    def __str__(self):
        return self.name


class Event(models.Model):
    """События."""

    name = models.CharField(
        verbose_name="Название события",
        max_length=200,
    )
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        verbose_name="Описание события", max_length=5000, blank=True
    )
    image = models.ImageField(
        verbose_name="Постер события",
        upload_to="establishment/images/event_posters/%Y-%m-%d",
        # upload_to="establishment/images/event",
    )
    date_start = models.DateTimeField(
        verbose_name="Начало события",
    )
    date_end = models.DateTimeField(
        verbose_name="Окончание события",
        blank=True,
        null=True,
    )
    type_event = models.ManyToManyField(
        TypeEvent,
        verbose_name="Тип события",
        blank=True,
    )
    price = models.PositiveSmallIntegerField(
        verbose_name="Цена события",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        default_related_name = "events"
        constraints = (
            models.UniqueConstraint(
                fields=("establishment_id", "name", "date_start"),
                name="unique_event_in_establishment_per_day",
            ),
        )

    def __str__(self):
        return f"{self.name}: {self.date_start} - {self.date_end}"


class EventPhoto(models.Model):
    """Фото события."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Событие",
    )
    image = models.ImageField(
        verbose_name="Файл фото",
        upload_to="establishment/images/event_photos/%Y-%m-%d",
    )

    class Meta:
        verbose_name = "Фотография события"
        verbose_name_plural = "Фотографии событий"

    def __str__(self):
        return f"Фото {self.id} - событие {self.event}"

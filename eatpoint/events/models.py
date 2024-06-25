from django.db import models

from establishments.models import Establishment


class TypeEvent(models.Model):
    """Тип события."""

    name = models.CharField(
        verbose_name="Тип события",
        max_length=200,
    )

    class Meta:
        verbose_name = "Тип события"
        verbose_name_plural = "Типы событий"

    def __str__(self):
        return self.name


class EventPhoto(models.Model):
    """Фото события."""

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name="Файл фото",
        upload_to="establishment/images/event_photos/%Y-%m-%d",
    )

    class Meta:
        verbose_name = "Фотография события"
        verbose_name_plural = "Фотографии событий"

    def __str__(self):
        return f"Фото события {self.id} в заведении {self.establishment}"


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
    cover_image = models.ForeignKey(
        EventPhoto,
        on_delete=models.PROTECT,
        verbose_name="Обложка события",
        related_name="covered_events",
    )
    date_start = models.DateTimeField(
        verbose_name="Начало события",
    )
    type_event = models.ManyToManyField(
        TypeEvent,
        verbose_name="Тип события",
    )
    price = models.PositiveSmallIntegerField(
        verbose_name="Цена события",
        blank=True,
        null=True,
    )
    photos = models.ManyToManyField(
        EventPhoto, blank=True, verbose_name="Фото события"
    )
    recur_settings = models.ForeignKey(
        "RecurSetting", on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        ordering = ("date_start",)
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
        return f"{self.date_start}: {self.name} в {self.establishment}"


class Reccurence(models.Model):
    """Периодичность повторения событий."""

    description = models.CharField(verbose_name="Описание", max_length=30)
    days = models.PositiveSmallIntegerField(
        verbose_name="Период в днях", unique=True
    )

    class Meta:
        ordering = ("days",)
        verbose_name = "Период повторения события"
        verbose_name_plural = "Периоды повторения событий"

    def __str__(self):
        return self.description


class RecurSetting(models.Model):
    """Настройки периодичности события."""

    recurrence = models.ForeignKey(
        Reccurence, on_delete=models.PROTECT, verbose_name="Частота повторений"
    )
    date_end = models.DateField(verbose_name="Дата последнего события")

    class Meta:
        verbose_name = "Настройки повторения событий"
        verbose_name_plural = "Настройки повторения событий"

    def __str__(self):
        return f"Настройки {self.recurrence} до {self.date_end}"

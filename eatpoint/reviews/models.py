from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from establishments.models import Establishment
from users.models import User


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
    )
    text = models.TextField(
        verbose_name="Текст отзыва",
        max_length=500,
    )
    created = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Допустимые значние 1-5"),
            MaxValueValidator(5, message="Допустимые значние 1-5"),
        ],
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["establishment", "author"], name="uniquereview"
            ),
        ]
        ordering = ["-created"]

    def __str__(self):
        return self.text


class OwnerResponse(models.Model):
    """Модель для ответа владельца на отзыв о заведении."""

    establishment_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_responses"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="owner_responses"
    )
    text = models.TextField(verbose_name="Текст ответа хозяина")
    created = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True
    )

    class Meta:
        verbose_name = "Ответ хозяина"
        verbose_name_plural = "Ответы хозяина"

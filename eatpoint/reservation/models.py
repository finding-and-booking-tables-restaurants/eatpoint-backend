from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from establishments.models import Establishment,TableEstablishment, Event

User = get_user_model()
# Create your models here.

class Restaurant_reservations(models.Model):
    """Список бронирований во всех ресторанах"""
    
    user = models.ForeignKey(
        User,
        related_name='reservation',
        on_delete=models.CASCADE,
    )
    email= models.EmailField(
        verbose_name="Электронная почта",
    )
    telephone = models.IntegerField(
        verbose_name="Телефон клиента",
        # validators=None,  # сделать валидатор для номера
    )
    establishment = models.ForeignKey(
        Establishment,
        related_name='reservation',
        verbose_name="Ресторан",
        on_delete=models.CASCADE,
    )
    table = models.ManyToManyField(
        TableEstablishment,
        related_name='reservation',
        verbose_name="Выбранный стол в ресторане",
    )
    Number_of_guests= models.CharField(
        verbose_name="Количество гостей",
        validators=[
            MinValueValidator(
                1, #заменить на константы
                message="Количество мест слишком маленькое",
                ),
            MaxValueValidator(
                100, # заменить на константы
                message="Количество мест слишком большое",
                ),
            ],
        )
    date_reservation= models.DateField(
        verbose_name="Дата бронирования",
    )
    start_time_reservation=models.TimeField(
        verbose_name="Время начала бронирования",
    )
    end_time_reservation = models.TimeField(
        verbose_name="Время окончания бронирования",
    )
    comment=models.CharField(
        verbose_name="Комментарий к бронированию",
    )
    reminder_one_day=models.BooleanField(
        verbose_name="Напоминание о бронировании за 1 день",
        default=False,
        )
    reminder_three_hours=models.BooleanField(
        verbose_name="Напоминание за 3 часа",
        default=False,
        )
    reminder_half_on_hour=models.BooleanField(
        verbose_name="Напоминание за 30 минут",
        default=False,
    )
    event=models.ManyToManyField(
        Event,
        verbose_name="Выбор события",
    )
    status = models.BooleanField(
        verbose_name="Статус бронирования Активен/Выполнен",   # Активен - True, Выполнен - False
        default=True,
    )
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


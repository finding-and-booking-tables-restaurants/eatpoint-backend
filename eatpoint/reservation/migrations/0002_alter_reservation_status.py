# Generated by Django 4.2.5 on 2023-11-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reservation", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="status",
            field=models.BooleanField(
                default=False,
                verbose_name="Статус бронирования Активен/Принят",
            ),
        ),
    ]
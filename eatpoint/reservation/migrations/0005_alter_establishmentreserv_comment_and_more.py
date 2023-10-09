# Generated by Django 4.2.5 on 2023-10-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reservation", "0004_rename_restaurant_reservations_establishmentreserv"),
    ]

    operations = [
        migrations.AlterField(
            model_name="establishmentreserv",
            name="comment",
            field=models.CharField(
                blank=True, max_length=200, verbose_name="Пожелания к заказу"
            ),
        ),
        migrations.AlterField(
            model_name="establishmentreserv",
            name="telephone",
            field=models.IntegerField(max_length=11, verbose_name="Телефон клиента"),
        ),
    ]

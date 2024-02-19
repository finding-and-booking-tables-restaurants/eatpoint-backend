# Generated by Django 4.2.5 on 2024-02-18 13:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "reservation",
            "0005_alter_reservation_telephone_alter_reservation_user",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="slot",
            options={
                "ordering": ["date", "time"],
                "verbose_name": "Свободный слот",
                "verbose_name_plural": "Свободные слоты",
            },
        ),
        migrations.AddField(
            model_name="reservation",
            name="is_deleted",
            field=models.BooleanField(
                default=False, verbose_name="Бронь отменена"
            ),
        ),
    ]
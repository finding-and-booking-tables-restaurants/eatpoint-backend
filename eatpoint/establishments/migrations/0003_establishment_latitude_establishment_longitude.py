# Generated by Django 4.2.5 on 2023-11-15 21:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("establishments", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="establishment",
            name="latitude",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Широта"
            ),
        ),
        migrations.AddField(
            model_name="establishment",
            name="longitude",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Долгота"
            ),
        ),
    ]

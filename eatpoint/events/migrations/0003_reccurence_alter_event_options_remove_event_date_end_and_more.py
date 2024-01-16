# Generated by Django 4.2.5 on 2023-12-28 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("establishments", "0009_table"),
        ("events", "0002_event_unique_event_in_establishment_per_day"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reccurence",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=30, verbose_name="Описание"),
                ),
                (
                    "days",
                    models.PositiveSmallIntegerField(
                        unique=True, verbose_name="Период в днях"
                    ),
                ),
            ],
            options={
                "verbose_name": "Период повторения события",
                "verbose_name_plural": "Периоды повторения событий",
                "ordering": ("days",),
            },
        ),
        migrations.AlterModelOptions(
            name="event",
            options={
                "default_related_name": "events",
                "ordering": ("date_start",),
                "verbose_name": "Событие",
                "verbose_name_plural": "События",
            },
        ),
        migrations.RemoveField(
            model_name="event",
            name="date_end",
        ),
        migrations.RemoveField(
            model_name="event",
            name="image",
        ),
        migrations.RemoveField(
            model_name="eventphoto",
            name="event",
        ),
        migrations.AddField(
            model_name="event",
            name="cover_image",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="covered_events",
                to="events.eventphoto",
                verbose_name="Обложка события",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="photos",
            field=models.ManyToManyField(
                blank=True, to="events.eventphoto", verbose_name="Фото события"
            ),
        ),
        migrations.AddField(
            model_name="eventphoto",
            name="establishment",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="establishments.establishment",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="event",
            name="type_event",
            field=models.ManyToManyField(
                to="events.typeevent", verbose_name="Тип события"
            ),
        ),
        migrations.CreateModel(
            name="RecurSetting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_end", models.DateField(verbose_name="Дата последнего события")),
                (
                    "recurrence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="events.reccurence",
                        verbose_name="Частота повторений",
                    ),
                ),
            ],
            options={
                "verbose_name": "Настройки повторения событий",
                "verbose_name_plural": "Настройки повторения событий",
            },
        ),
        migrations.AddField(
            model_name="event",
            name="recur_settings",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="events.recursetting",
            ),
        ),
    ]

# Generated by Django 4.2.5 on 2023-10-12 13:41

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("reservation", "0003_alter_reservation_telephone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="telephone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                default=None, max_length=128, null=True, region=None
            ),
        ),
    ]

# Generated by Django 4.1.2 on 2023-01-24 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_address"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userbase",
            name="address_line_1",
        ),
        migrations.RemoveField(
            model_name="userbase",
            name="address_line_2",
        ),
        migrations.RemoveField(
            model_name="userbase",
            name="postcode",
        ),
        migrations.RemoveField(
            model_name="userbase",
            name="town_city",
        ),
    ]

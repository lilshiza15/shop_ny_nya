# Generated by Django 4.1.2 on 2023-01-27 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="country_code",
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name="order",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_option",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]

# Generated by Django 2.2.12 on 2021-01-07 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0008_bookings_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
# Generated by Django 2.2.12 on 2021-02-19 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0014_bookings_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]

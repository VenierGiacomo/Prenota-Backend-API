# Generated by Django 2.2.12 on 2020-09-07 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_bookings_store_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='service_n',
            field=models.TextField(blank=True, null=True),
        ),
    ]
# Generated by Django 2.2.12 on 2021-03-22 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0015_auto_20210219_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='end_t',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookings',
            name='start_t',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

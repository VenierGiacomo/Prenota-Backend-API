# Generated by Django 2.2.12 on 2020-06-17 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='phone',
            field=models.TextField(blank=True, null=True),
        ),
    ]

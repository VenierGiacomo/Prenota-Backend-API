# Generated by Django 2.2.12 on 2021-01-21 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_store_lat_long'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='stripe_connect',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

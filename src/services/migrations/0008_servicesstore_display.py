# Generated by Django 2.2.12 on 2020-10-28 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20201002_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesstore',
            name='display',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 2.2.12 on 2020-08-04 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20200713_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='max_spots',
            field=models.IntegerField(default=-1),
        ),
    ]
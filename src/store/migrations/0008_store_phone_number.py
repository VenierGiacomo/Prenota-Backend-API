# Generated by Django 2.2.12 on 2020-08-11 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_store_max_spots'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 2.2.12 on 2020-08-31 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_remove_servicesstore_duration_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesstore',
            name='duration_book',
            field=models.IntegerField(null=True),
        ),
    ]
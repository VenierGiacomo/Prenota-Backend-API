# Generated by Django 2.2.12 on 2020-07-08 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesstore',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
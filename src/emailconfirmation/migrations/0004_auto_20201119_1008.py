# Generated by Django 2.2.12 on 2020-11-19 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailconfirmation', '0003_registerconfirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='service',
            field=models.CharField(max_length=100),
        ),
    ]

# Generated by Django 2.2.12 on 2021-02-26 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopclients', '0007_storeclient_ismember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeclient',
            name='note',
            field=models.TextField(default=''),
        ),
    ]

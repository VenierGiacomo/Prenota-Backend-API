# Generated by Django 2.2.12 on 2021-02-08 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopclients', '0005_auto_20210208_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeclient',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]

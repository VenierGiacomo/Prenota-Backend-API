# Generated by Django 2.2.12 on 2021-03-22 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_auto_20210319_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 2.2.12 on 2020-07-13 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_store_business_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='business_type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 2.2.12 on 2021-01-22 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_store_stripe_connect'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='payable',
            field=models.BooleanField(default=False),
        ),
    ]

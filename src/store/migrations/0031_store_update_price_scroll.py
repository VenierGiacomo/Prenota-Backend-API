# Generated by Django 2.2.12 on 2021-04-26 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_store_has_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='update_price_scroll',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 2.2.12 on 2021-04-26 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services_category', '0001_initial'),
        ('services', '0012_auto_20210201_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesstore',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='services_category.ServiceCategory'),
        ),
        migrations.AddField(
            model_name='servicesstore',
            name='favorite',
            field=models.BooleanField(default=True),
        ),
    ]

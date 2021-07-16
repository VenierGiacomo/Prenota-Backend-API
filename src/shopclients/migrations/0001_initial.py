# Generated by Django 2.2.12 on 2020-07-15 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0006_auto_20200713_1051'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.TextField()),
                ('hair_color', models.TextField(blank=True, null=True)),
                ('hair_lenght', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('avarage_expense', models.TextField(blank=True, null=True)),
                ('last_service', models.TextField()),
                ('service_n', models.TextField()),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('shop', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='store.Store')),
            ],
        ),
    ]
# Generated by Django 2.2.12 on 2020-05-25 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('day', models.IntegerField()),
                ('week', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('client_name', models.TextField()),
                ('details', models.TextField()),
                ('service_n', models.TextField()),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking_employee', to=settings.AUTH_USER_MODEL)),
                ('shop', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='store.Store')),
            ],
        ),
    ]

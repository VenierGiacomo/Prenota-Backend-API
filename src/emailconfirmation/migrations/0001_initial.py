# Generated by Django 2.2.12 on 2020-06-30 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Emailconfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('day', models.IntegerField()),
                ('month', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('time', models.CharField(max_length=50)),
                ('service', models.CharField(max_length=50)),
            ],
        ),
    ]

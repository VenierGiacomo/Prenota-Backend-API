# Generated by Django 2.2.12 on 2021-04-08 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_auto_20210329_1233'),
        ('serviceaddons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceaddon',
            name='shop_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.Store'),
        ),
    ]

# Generated by Django 3.2.16 on 2023-11-22 15:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='date_time_end_sending',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 15, 4, 19, 851033, tzinfo=utc), verbose_name='Конец рассылки'),
        ),
    ]
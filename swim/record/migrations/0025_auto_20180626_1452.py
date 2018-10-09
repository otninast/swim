# Generated by Django 2.0.6 on 2018-06-26 05:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0024_auto_20180623_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='impression',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='感想'),
        ),
        migrations.AddField(
            model_name='training',
            name='point',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='点数'),
        ),
        migrations.AlterField(
            model_name='result_time',
            name='rest',
            field=models.NullBooleanField(default=False, verbose_name='レスト'),
        ),
        migrations.AlterField(
            model_name='training',
            name='date',
            field=models.DateField(default=datetime.date(2018, 6, 26), null=True),
        ),
    ]
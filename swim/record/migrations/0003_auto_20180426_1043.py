# Generated by Django 2.0.3 on 2018-04-26 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0002_auto_20180426_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='period',
            field=models.IntegerField(verbose_name='期'),
        ),
    ]

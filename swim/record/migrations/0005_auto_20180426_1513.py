# Generated by Django 2.0.3 on 2018-04-26 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0004_menue_time_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menue',
            old_name='menue',
            new_name='menue_name',
        ),
        migrations.AlterField(
            model_name='menue',
            name='count',
            field=models.IntegerField(verbose_name='本数'),
        ),
        migrations.AlterField(
            model_name='menue',
            name='distance',
            field=models.IntegerField(verbose_name='距離'),
        ),
    ]

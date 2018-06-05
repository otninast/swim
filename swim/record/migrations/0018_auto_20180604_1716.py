# Generated by Django 2.0.3 on 2018-06-04 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0017_auto_20180604_1323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='training',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='result_time',
            name='traning_id',
        ),
        migrations.AddField(
            model_name='result_time',
            name='training',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='time', to='record.Training'),
        ),
        migrations.AlterField(
            model_name='result_time',
            name='time_minutes',
            field=models.IntegerField(default=0, verbose_name='分'),
        ),
        migrations.AlterField(
            model_name='result_time',
            name='time_seconds',
            field=models.IntegerField(default=0, verbose_name='秒'),
        ),
        migrations.AlterField(
            model_name='result_time',
            name='time_seconds_micro',
            field=models.IntegerField(default=0, verbose_name='コンマ秒'),
        ),
    ]

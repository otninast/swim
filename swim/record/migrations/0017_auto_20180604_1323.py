# Generated by Django 2.0.3 on 2018-06-04 04:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_logentry_remove_auto_add'),
        ('record', '0016_auto_20180531_0636'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.RemoveField(
            model_name='users',
            name='user_ptr',
        ),
        migrations.AlterField(
            model_name='training',
            name='date',
            field=models.DateField(default=datetime.date(2018, 6, 4), null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]

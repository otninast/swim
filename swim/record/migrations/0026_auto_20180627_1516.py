# Generated by Django 2.0.6 on 2018-06-27 06:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('record', '0025_auto_20180626_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Man'), ('W', 'Woman'), ('O', 'Other')], max_length=5, null=True, verbose_name='性別')),
                ('generation', models.PositiveIntegerField(blank=True, null=True, verbose_name='期')),
                ('style', models.CharField(blank=True, choices=[('Fr', 'Fr'), ('Ba', 'Ba'), ('Br', 'Br'), ('Fly', 'Fly'), ('IM', 'IM')], max_length=10, null=True)),
                ('cource', models.PositiveIntegerField(blank=True, null=True, verbose_name='コース')),
                ('is_manager', models.BooleanField(default=False, verbose_name='マネジャー')),
                ('is_courch', models.BooleanField(default=False, verbose_name='コーチ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='training',
            name='date',
            field=models.DateField(default=datetime.date(2018, 6, 27), null=True),
        ),
    ]

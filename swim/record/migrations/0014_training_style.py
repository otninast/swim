# Generated by Django 2.0.3 on 2018-05-30 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0013_auto_20180529_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='style',
            field=models.CharField(choices=[('Fr', 'Fr'), ('Ba', 'Ba'), ('Br', 'Br'), ('Fly', 'Fly'), ('IM', 'IM')], max_length=10, null=True),
        ),
    ]

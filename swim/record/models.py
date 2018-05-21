from django.db import models

SEX_CHOICES = (
    ('M', 'Man'),
    ('W', 'Woman'),
)

STYLE_CHOICES = (
    ('Fr', 'Fr'),
    ('Ba', 'Ba'),
    ('Br', 'Br'),
    ('Fly', 'Fly'),
    ('IM', 'IM'),

)

DISTANCE_CHOICES = (
    (25, 25),
    (50, 50),
    (100, 100),
    (200, 200),
    (400, 400),
    (800, 800),
)

# MENUE_CHOICES = (
#     ('', ''),
#     ('', ''),
#     ('', ''),
#     ('', ''),
#     ('', ''),
#     ('', ''),
#     ('', ''),
# )

class Person(models.Model):
    family_name = models.CharField(max_length=15, verbose_name='姓')
    last_name = models.CharField(max_length=15, verbose_name='名')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='性別')
    period = models.IntegerField(verbose_name='期')
    style = models.CharField(choices=STYLE_CHOICES, max_length=4,  verbose_name='スタイル')

    is_manager = models.BooleanField(default=False, verbose_name='マネジャー')
    is_OBOG = models.BooleanField(default=False, verbose_name='既卒')
    is_courch = models.BooleanField(default=False, verbose_name='コーチ')
    is_master = models.BooleanField(default=False, verbose_name='管理者')

class Menue(models.Model):
    menue_name = models.CharField(max_length=15, verbose_name='メニュー')
    distance = models.IntegerField(choices=DISTANCE_CHOICES, verbose_name='距離')
    # count = models.IntegerField(verbose_name='本数')

class Time_Result(models.Model):
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    menue = models.ForeignKey(Menue, on_delete=models.SET_NULL, null=True)
    time_result = models.DurationField(verbose_name='タイム')








# class Record(models.Model):
#     content = models.CharField(max_length=140, verbose_name='本文')


from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User

from datetime import date

SEX_CHOICES = (
    ('M', 'Man'),
    ('W', 'Woman'),
    ('O', 'Other')
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

ONE_TO_TEN_CHOICES  = [
    (num, num) for num in range(0, 11)
]

ONE_TO_SIXTY_CHOICE = [
    (num, num) for num in range(0, 60)
]


class Menue(models.Model):
    menue_name = models.CharField(max_length=15, verbose_name='メニュー')
    def __str__(self):
        return self.menue_name

class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    menue_name = models.ForeignKey(Menue, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=date.today(), null=True, blank=False)
    style = models.CharField(choices=STYLE_CHOICES, max_length=10, null=True, blank=False)
    distance = models.IntegerField(choices=DISTANCE_CHOICES, null=True)

    point = models.PositiveIntegerField('点数', null=True, blank=True)
    impression = models.TextField('感想', max_length=1000, null=True, blank=True)
    def __str__(self):
        return '{}, {}, {}'.format(self.user.username, self.date, self.menue_name)

class Result_Time(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, null=True, blank=True)
    num_of_swim = models.IntegerField('本数', null=True)
    second = models.FloatField('タイム[s]', null=True, blank=True)
    time_str = models.CharField('タイム', max_length=15, null=True, blank=True)
    rest = models.NullBooleanField('レスト', blank=True, default=False)
    def __str__(self):
        return '{}, {}'.format(self.training, self.num_of_swim)

class User_Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    familyname = models.CharField('姓', max_length=15, null=True, blank=True)
    firstname = models.CharField('名', max_length=15, null=True, blank=True)
    sex = models.CharField('性別', max_length=5, choices=SEX_CHOICES, null=True, blank=True)
    generation = models.PositiveIntegerField('期', null=True, blank=True)
    style = models.CharField(choices=STYLE_CHOICES, max_length=10, null=True, blank=True)
    cource = models.PositiveIntegerField('コース', null=True, blank=True)
    is_manager = models.BooleanField('マネジャー', default=False)
    is_courch = models.BooleanField('コーチ', default=False)
    def __str__(self):
        return self.user.username







# class Record(models.Model):
#     content = models.CharField(max_length=140, verbose_name='本文')

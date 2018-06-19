from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User, AbstractBaseUser

# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.base_user import AbstractBaseUser

from django.utils.translation import ugettext_lazy as _

from datetime import date

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

ONE_TO_TEN_CHOICES  = [
    (num, num) for num in range(0, 11)
]

ONE_TO_SIXTY_CHOICE = [
    (num, num) for num in range(0, 60)
]

# class Users(AbstractBaseUser):
#     username = models.CharField('ユーザー名', max_length=30, unique=True)
#     screenname = models.CharField('ユーザー名（表示用）', max_length=255)
#     USERNAME_FIELD = 'username'
#
#     sex = models.CharField(choices=SEX_CHOICES, max_length=5, null=True, blank=False)
#     generation = models.IntegerField(default=47, null=True, blank=False)
#     def __str__(self):
#         return self.username



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
    def __str__(self):
        return '{}, {}, {}'.format(self.user.username, self.date, self.menue_name.menue_name)

    #     label = '{0.menue_name} {0.self.date}'
    #     return label.format(self)

class Result_Time(models.Model):
    # training = models.OneToOneField(Training, on_delete=models.CASCADE, null=True, blank=True, related_name='time')
    training = models.ForeignKey(Training, on_delete=models.CASCADE, null=True, blank=True)
    # time_minutes = models.IntegerField(verbose_name='分', default=0)
    # time_seconds = models.IntegerField(verbose_name='秒', default=0)
    # time_seconds_micro = models.IntegerField(verbose_name='コンマ秒', default=0)
    num_of_swim = models.IntegerField('本数', null=True)
    second = models.FloatField('タイム[s]', null=True, blank=True)
    rest = models.BooleanField('レスト', blank=True, default=False)
    def __str__(self):
        return '{}, {}'.format(self.training, self.num_of_swim)
        # label = '{0.training.menue_name}  {0.self.training.date}'
        # return label.format(self)



# class Person(models.Model):
#     family_name = models.CharField(max_length=15, verbose_name='姓')
#     last_name = models.CharField(max_length=15, verbose_name='名')
#     sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='性別')
#     period = models.IntegerField(verbose_name='期')
#     style = models.CharField(choices=STYLE_CHOICES, max_length=4,  verbose_name='スタイル')
#
#     is_manager = models.BooleanField(default=False, verbose_name='マネジャー')
#     is_OBOG = models.BooleanField(default=False, verbose_name='既卒')
#     is_courch = models.BooleanField(default=False, verbose_name='コーチ')
#     is_master = models.BooleanField(default=False, verbose_name='管理者')






# class Record(models.Model):
#     content = models.CharField(max_length=140, verbose_name='本文')

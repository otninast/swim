
from django.db import models
# from django.core.mail import send_mail
from django.contrib.auth.models import User

# from datetime import date
from django.utils import timezone
# from record import views

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

ONE_TO_TEN_CHOICES = [
    (num, num) for num in range(0, 11)
]

ONE_TO_SIXTY_CHOICE = [
    (num, num) for num in range(0, 60)
]


class Menue(models.Model):
    menue_name = models.CharField(max_length=15, verbose_name='メニュー')

    def __str__(self):
        return self.menue_name


class DayMenu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=False)
    score = models.PositiveIntegerField('点数', null=True, blank=True)
    reflection = models.TextField('感想', max_length=1000, null=True, blank=True)

    def get_trainings(self):
        t = TrainingMenu.objects.filter(daymenu=self)
        return [i for i in t]

    def __str__(self):
        return '{}, {}, {}'.format(self.pk, self.user, self.date)


class TrainingMenu(models.Model):
    daymenu = models.ForeignKey(DayMenu, on_delete=models.CASCADE, null=True, blank=True, related_name='trainingmenus')
    order = models.PositiveIntegerField('メニューNo.', null=True, blank=True)
    menu_name = models.ForeignKey(Menue, on_delete=models.CASCADE, null=True, blank=True)
    style = models.CharField(choices=STYLE_CHOICES, max_length=10, null=True, blank=False)
    distance = models.IntegerField(choices=DISTANCE_CHOICES, null=False)
    # graph = views.make_img()

    def get_times(self):
        t = Result_Time.objects.filter(trainingmenu=self)
        return [i.time for i in t]

    def __str__(self):
        return '{}, {}'.format(self.daymenu.pk, self.menu_name)


class Result_Time(models.Model):
    trainingmenu = models.ForeignKey(TrainingMenu, on_delete=models.CASCADE, null=True, blank=True, related_name='times')
    order = models.IntegerField('本数', null=True)
    time = models.FloatField('タイム[s]', null=True, blank=True)
    rest = models.NullBooleanField('レスト', blank=True, default=False)


    def __str__(self):
        return '{}'.format(self.order)


class Rap_Time(models.Model):
    result_time = models.ForeignKey(Result_Time, on_delete=models.CASCADE, null=True, blank=True, related_name='raps')
    time = models.FloatField('タイム[s]', null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(int(self.pk)*50, self.time)


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

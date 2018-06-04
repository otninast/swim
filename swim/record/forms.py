from django import forms
from django.contrib.auth.models import User

from .models import Person, Menue, Training, Result_Time, Users

import pandas as pd
df = pd.read_csv('~/swimrecord/swim/record/Result_all.csv')





# class Users_Form(forms.ModelForm):
#     class Meta:
#         model = User
#         # fields = '__all__'
#         exclude = ['user_permissions', 'is_staff', 'groups', 'is_active', 'is_superuser', 'last_login', 'date_joined']

class Menue_Form(forms.ModelForm):
    class Meta:
        model = Menue
        fields = '__all__'

class Training_Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'
        menue_name = forms.ModelChoiceField(Menue.objects)

class Result_Time_Form(forms.ModelForm):
    class Meta:
        model = Result_Time
        fields = '__all__'
        widgets = {
            'time_minutes': forms.NumberInput(attrs={
                'name': 'time_minutes[]',
            }),
            'time_seconds': forms.NumberInput(attrs={
                'name': 'time_seconds[]',
            }),
            'time_seconds_micro': forms.NumberInput(attrs={
                'name': 'time_seconds_micro[]',
            }),
        }


class Select_Form(forms.Form):
    year_list = sorted(list(set(df.Year.values)))
    style_list = sorted(list(set(df.Style.values)))
    distance_list = sorted(list(set(df.Distance.values)))
    sex_list = sorted(list(set(df.Sex.values)))

    YEAR_CHOICES = [(year, year) for year in year_list]
    STYLE_CHOICES = [(style, style) for style in style_list]
    DISTANCE_CHOICES = [(distance, distance) for distance in distance_list]
    SEX_CHOICES = [(sex, sex) for sex in sex_list]

    YEAR_CHOICES.append((year_list, 'all'))
    STYLE_CHOICES.append((style_list, 'all'))
    DISTANCE_CHOICES.append((distance_list, 'all'))
    SEX_CHOICES.append((sex_list, 'all'))


    year = forms.ChoiceField(choices=YEAR_CHOICES, label='年度')
    sex = forms.ChoiceField(choices=SEX_CHOICES, label='性別')
    style = forms.ChoiceField(choices=STYLE_CHOICES, label='スタイル')
    # sex = forms.MultipleChoiceField(choices=SEX_CHOICES, label='性別', widget=forms.CheckboxSelectMultiple())
    # style = forms.ChoiceField(choices=STYLE_CHOICES, label='スタイル')
    distance = forms.ChoiceField(choices=DISTANCE_CHOICES, label='距離')







# sex = Df.Sex.unique()

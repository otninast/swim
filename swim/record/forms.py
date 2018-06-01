from django import forms
from .models import Person, Menue, Training, Result_Time, Users

import pandas as pd
df = pd.read_csv('~/swimrecord/swim/record/Result_all.csv')





class Users_Form(forms.ModelForm):
    class Meta:
        model = Users
        # fields = '__all__'
        exclude = ['user_permissions', 'is_staff', 'groups', 'is_active', 'is_superuser', 'last_login', 'date_joined']

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
        # widgets = {
        #     'time_minutes': forms.NumberInput(attrs={'step': 1}),
        #     'time_seconds': forms.NumberInput(attrs={'step': 1}),
        #     'time_seconds_micro': forms.NumberInput(attrs={'step': 1})
        # }

class Select_Form(forms.Form):
    YEAR_CHOICES = [(year, year) for year in  set(df.Year.values)]
    STYLE_CHOICES = [(style, style) for style in  set(df.Style.values)]
    DISTANCE_CHOICES = [(distance, distance) for distance in set(df.Distance.values)]
    SEX_CHOICES = [(sex, sex) for sex in list(set(df.Sex.values))]

    year = forms.ChoiceField(choices=YEAR_CHOICES, label='年度')
    sex = forms.MultipleChoiceField(choices=SEX_CHOICES, label='性別', widget=forms.CheckboxSelectMultiple())
    style = forms.ChoiceField(choices=STYLE_CHOICES, label='スタイル')
    distance = forms.ChoiceField(choices=DISTANCE_CHOICES, label='距離')







# sex = Df.Sex.unique()

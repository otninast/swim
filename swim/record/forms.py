from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Menue, DayMenu, TrainingMenu, Result_Time, User_Info
import os
import pandas as pd


path = os.path.join(os.path.join(os.path.dirname(__file__), 'Result_all.csv'))
df = pd.read_csv(path)


class User_Info_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(User_Info_Form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User_Info
        # fields = '__all__'
        exclude = ['user', 'is_manager', 'is_courch', ]


class User_Update_Form(User_Info_Form, UserChangeForm):

    class Meta:
        model = User
        # model = User_Info
        fields = '__all__'
        # exclude = ['user', 'is_manager', 'is_courch', ]


class Menue_Form(forms.ModelForm):
    class Meta:
        model = Menue
        fields = '__all__'


class DayMenu_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DayMenu_Form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = DayMenu
        fields = '__all__'


class TrainingMenu_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrainingMenu_Form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TrainingMenu
        fields = '__all__'
        # menue_name = forms.ModelChoiceField(Menue.objects)


class Result_Time_Form(forms.ModelForm):
    NUMBER = [
        (num, num) for num in range(0, 10)
    ]
    m_10 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'm_10 custom-select'}))
    m_1 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'm_1 custom-select'}))
    s_10 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_10 custom-select'}))
    s_1 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_1 custom-select'}))
    ms_10 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_10 custom-select'}))
    ms_1 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_1 custom-select'}))

    rest = forms.BooleanField(required=False)

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


class Rap_Time_Form(forms.Form):

    NUMBER = [
        (num, num) for num in range(0, 10)
    ]

    m_1_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'm_1_r custom-select'}))
    s_10_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_10_r custom-select'}))
    s_1_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_1_r custom-select'}))
    ms_10_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_10_r custom-select'}))
    ms_1_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_1 custom-select'}))


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


    year = forms.ChoiceField(choices=YEAR_CHOICES, label='年度', widget=forms.Select(attrs={'class': 'year custom-select'}))
    sex = forms.ChoiceField(choices=SEX_CHOICES, label='性別', widget=forms.Select(attrs={'class': 'sex custom-select'}))
    style = forms.ChoiceField(choices=STYLE_CHOICES, label='スタイル', widget=forms.Select(attrs={'class': 'style custom-select'}))
    # sex = forms.MultipleChoiceField(choices=SEX_CHOICES, label='性別', widget=forms.CheckboxSelectMultiple())
    # style = forms.ChoiceField(choices=STYLE_CHOICES, label='スタイル')
    distance = forms.ChoiceField(choices=DISTANCE_CHOICES, label='距離', widget=forms.Select(attrs={'class': 'distance custom-select'}))






# class Menu_Test_Form(forms.Form):
#     from record.models import STYLE_CHOICES, DISTANCE_CHOICES
#
#     date = forms.DateField(initial=timezone.now, widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
#
#     menu = forms.ChoiceField(choices=[(i.menue_name, i.menue_name) for i in Menue.objects.all()], widget=forms.Select(attrs={'class': 'custom-select'}))
#
#     style = forms.ChoiceField(choices=STYLE_CHOICES, widget=forms.Select(attrs={'class': 'custom-select'}))
#     distance = forms.ChoiceField(choices=DISTANCE_CHOICES, widget=forms.Select(attrs={'class': 'custom-select'}))
#     number = forms.ChoiceField(choices=[(num, num) for num in range(1, 31)], widget=forms.Select(attrs={'class': 'custom-select'}))
#     score = forms.ChoiceField(choices=[(num, num) for num in range(1, 6)], widget=forms.Select(attrs={'class': 'custom-select'}))
#     reflection = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}))




# class Time_Form(forms.Form):
#     NUMBER = [
#         (num, num) for num in range(0, 10)
#     ]
#
#     m_10 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'm_10 custom-select'}))
#     m_1 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'm_1 custom-select'}))
#     s_10 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_10 custom-select'}))
#     s_1 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_1 custom-select'}))
#     ms_10 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_10 custom-select'}))
#     ms_1 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_1 custom-select'}))
#
#     rest = forms.BooleanField(required=False)


# class Rap_Form(forms.Form):
#     NUMBER = [
#         (num, num) for num in range(0, 10)
#     ]
#
#     m_1_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'm_1_r custom-select'}))
#     s_10_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_10_r custom-select'}))
#     s_1_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_1_r custom-select'}))
#     ms_10_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_10_r custom-select'}))
#     ms_1_r = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_1 custom-select'}))

# class Sample_Form(forms.Form):
#     def __init__(self, num=3, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(self.num):
#             self['value_{}'.format(i)] = forms.CharField(max_length=10)

    # NUMBER = [
    #     (num, num) for num in range(0, 10)
    # ]
    #
    # m_10 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'm_10 custom-select'}))
    # m_1 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'm_1 custom-select'}))
    # s_10 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_10 custom-select'}))
    # s_1 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 's_1 custom-select'}))
    # ms_10 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_10 custom-select'}))
    # ms_1 = forms.ChoiceField(choices=NUMBER, widget=forms.Select(attrs={'class': 'ms_1 custom-select'}))
    #
    # rest = forms.BooleanField(required=False)

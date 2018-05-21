from django import forms
from .models import Person, Menue, Time_Result

class Menue_Form(forms.ModelForm):
    class Meta:
        model = Menue
        fields = '__all__'


class Time_Result_Form(forms.ModelForm):
    class Meta:
        model = Time_Result
        fields = '__all__'

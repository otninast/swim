from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Tex

class TexForm(forms.ModelForm):
    class Meta:
        model = Tex
        fields = '__all__'

# class UserCreationForm

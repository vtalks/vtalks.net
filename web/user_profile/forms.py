from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class AuthUserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AuthProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']

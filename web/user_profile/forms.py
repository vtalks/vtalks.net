from django import forms


class UserPreferences(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea)

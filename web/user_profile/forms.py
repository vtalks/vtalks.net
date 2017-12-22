from django import forms


class AuthProfileSettingsForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    bio = forms.CharField(label='Biography', widget=forms.Textarea, required=False)

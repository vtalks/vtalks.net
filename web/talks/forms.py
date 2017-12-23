from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label='Search query', max_length=200)

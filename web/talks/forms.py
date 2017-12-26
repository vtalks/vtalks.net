from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(max_length=200, initial="")

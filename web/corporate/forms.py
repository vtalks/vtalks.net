from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        """Sends email using the self.cleaned_data dictionary"""
        print(self.cleaned_data)
        # TODO:
        # - Send email to hello@vtalks.net

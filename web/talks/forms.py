from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary

        print(self.cleaned_data)

        # TODO:
        # - Send email using an external service
        """
        send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['hello@vtalks.net'],
            fail_silently=False,
        )
        """

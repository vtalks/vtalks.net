import requests

from django.conf import settings
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def save(self):
        request_url = 'https://api.mailgun.net/v3/mg.vtalks.net/messages'
        requests.post(request_url,
                      auth=('api', settings.EMAIL_HOST_PASSWORD),
                      data={
                          'from': 'hello@example.com',
                          'to': 'hello@vtalks.net',
                          'subject': 'Hello',
                          'text': 'Hello from Mailgun',
                      })

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render
from django.core.mail import send_mail

from .forms import ContactForm

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(View):
    template_name = 'contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                ['hello@vtalks.net'],
                fail_silently=True
            )
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class HelpView(TemplateView):
    template_name = 'help.html'


class TermsView(TemplateView):
    template_name = 'terms.html'


class PrivacyView(TemplateView):
    template_name = 'privacy.html'

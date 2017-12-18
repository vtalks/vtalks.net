from django.views.generic import TemplateView
from django.shortcuts import render

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class HelpView(TemplateView):
    template_name = 'help.html'

class TermsView(TemplateView):
    template_name = 'terms.html'

class PrivacyView(TemplateView):
    template_name = 'privacy.html'

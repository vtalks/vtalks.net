from django.views.generic import TemplateView
from django.views.generic import FormView

from .forms import ContactForm

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '.'

    def form_valid(self, form):
        form.save()
        return super(ContactView, self).form_valid(form)


class HelpView(TemplateView):
    template_name = 'help.html'


class TermsView(TemplateView):
    template_name = 'terms.html'


class PrivacyView(TemplateView):
    template_name = 'privacy.html'

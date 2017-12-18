from django.views.generic import TemplateView
from django.views.generic import FormView

from .forms import ContactForm

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)


class HelpView(TemplateView):
    template_name = 'help.html'


class TermsView(TemplateView):
    template_name = 'terms.html'


class PrivacyView(TemplateView):
    template_name = 'privacy.html'

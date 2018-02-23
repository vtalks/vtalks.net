from django.urls import path

from .views import AboutView
from .views import ContactView
from .views import HelpView
from .views import TermsView
from .views import PrivacyView
from .views import TemplateView

app_name = 'corporate'
urlpatterns = [
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('help', HelpView.as_view(), name='help'),
    path('terms', TermsView.as_view(), name='terms'),
    path('privacy', PrivacyView.as_view(), name='privacy'),

    path('404', TemplateView.as_view(template_name="404.html"), name='404'),
    path('500', TemplateView.as_view(template_name="500.html"), name='500'),
]
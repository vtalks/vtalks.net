from django.urls import path

from django.views.generic import TemplateView

from .views import IndexView

app_name = 'home'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    path('404', TemplateView.as_view(template_name="404.html"), name='404'),
    path('500', TemplateView.as_view(template_name="500.html"), name='500'),
]

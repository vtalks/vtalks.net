from django.views.generic import TemplateView
from django.shortcuts import render

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
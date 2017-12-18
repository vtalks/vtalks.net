"""vtalks.net URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import include

from django.contrib import admin

from talks.views import IndexView

from talks.views import AboutView
from talks.views import ContactView
from talks.views import HelpView
from talks.views import TermsView
from talks.views import PrivacyView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('user_profile.urls')),

    path('', IndexView.as_view(), name='index'),

    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('help', HelpView.as_view(), name='help'),
    path('terms', TermsView.as_view(), name='terms'),
    path('privacy', PrivacyView.as_view(), name='privacy'),
]

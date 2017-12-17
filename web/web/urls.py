"""web URL Configuration

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
from django.contrib import admin
from django.urls import path

from talks.views import IndexView
from user_profile.views import LogoutView
from user_profile.views import LoginView
from user_profile.views import AuthTwitterView
from user_profile.views import AuthTwitterCallbackView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view(), name='index'),

    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/twitter', AuthTwitterView.as_view(), name='auth_twitter'),
    path('auth/twitter/callback', AuthTwitterCallbackView.as_view(), name='auth_twitter_callback'),
]

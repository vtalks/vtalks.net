from django.urls import path

from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

from .views import AuthTwitterView
from .views import AuthTwitterCallbackView
from .views import AuthProfileSettingsView

app_name = 'user_profile'
urlpatterns = [
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),

    path('settings', AuthProfileSettingsView.as_view(), name='settings'),

    path('twitter', AuthTwitterView.as_view(), name='auth_twitter'),
    path('twitter/callback', AuthTwitterCallbackView.as_view(), name='auth_twitter_callback'),
]

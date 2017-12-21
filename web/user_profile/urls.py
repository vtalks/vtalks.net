from django.urls import path

from .views import AuthTwitterView
from .views import AuthTwitterCallbackView
from django.contrib.auth.views import logout
from django.contrib.auth.views import login

app_name = 'user_profile'
urlpatterns = [
    path('logout', logout, {'next_page': '/'}, name='logout'),
    path('login', login, name='login'),
    path('twitter', AuthTwitterView.as_view(), name='auth_twitter'),
    path('twitter/callback', AuthTwitterCallbackView.as_view(),
         name='auth_twitter_callback'),
]

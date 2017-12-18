from django.urls import path

from .views import LogoutView
from .views import LoginView
from .views import AuthTwitterView
from .views import AuthTwitterCallbackView

app_name = 'user_profile'
urlpatterns = [
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
    path('twitter', AuthTwitterView.as_view(), name='auth_twitter'),
    path('twitter/callback', AuthTwitterCallbackView.as_view(),
         name='auth_twitter_callback'),
]

from django.urls import path
from django.urls import include

from rest_framework import routers

from .views import ChannelViewSet

router = routers.DefaultRouter()
router.register(r'channels', ChannelViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]

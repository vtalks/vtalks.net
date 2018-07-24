from django.urls import path
from django.urls import include

from rest_framework import routers

from talks.api import TalkViewSet
from talks.api import RandomTalkView
from channels.api import ChannelViewSet
from playlists.api import PlaylistViewSet

router = routers.DefaultRouter()
router.register(r'talk', TalkViewSet)
router.register(r'channel', ChannelViewSet)
router.register(r'playlist', PlaylistViewSet)

urlpatterns = [
    path('talk/random-talk/', RandomTalkView.as_view(), name='random-talk'),
    path('', include(router.urls)),
]

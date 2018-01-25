from django.urls import path
from django.urls import re_path
from django.urls import include

from .views import IndexView
from .views import LatestTalksView
from .views import BestTalksView
from .views import SearchTalksView
from .views import DetailTalkView
from .views import LikeTalkView
from .views import DetailTagView

from rest_framework import routers

from .api import ChannelViewSet
from .api import PlaylistViewSet
from .api import TalkViewSet

router = routers.DefaultRouter()
router.register(r'channel', ChannelViewSet)
router.register(r'playlist', PlaylistViewSet)
router.register(r'talk', TalkViewSet)

app_name = 'talks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('latest', LatestTalksView.as_view(), name='latest-talks'),
    re_path(r'^latest/page/(?P<page>\d+)/$', LatestTalksView.as_view(), name='latest-talks-paginated'),

    path('best', BestTalksView.as_view(), name='best-talks'),
    re_path(r'^best/page/(?P<page>\d+)/$', BestTalksView.as_view(), name='best-talks-paginated'),

    path('search', SearchTalksView.as_view(), name='search'),

    path('talk/<slug:slug>/', DetailTalkView.as_view(), name='talk-details'),
    path('talk/<slug:slug>/like', LikeTalkView.as_view(), name='talk-like'),

    path('tag/<slug:slug>/', DetailTagView.as_view(), name='tag-details'),
    path('tag/<slug:slug>/page/<int:page>/', DetailTagView.as_view(), name='tag-details-paginated'),

    path('api/', include(router.urls)),
]
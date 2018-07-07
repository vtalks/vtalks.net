from django.urls import path
from django.urls import re_path

from .views import LatestTalksView
from .views import BestTalksView
from .views import DetailTalkView
from .views import LikeTalkView
from .views import DislikeTalkView
from .views import FavoriteTalkView
from .views import WatchTalkView
from .views import RSSLatestView

app_name = 'talks'
urlpatterns = [
    path('rss/latest', RSSLatestView(), name='latest-feed'),

    path('latest', LatestTalksView.as_view(), name='latest-talks'),
    re_path(r'^latest/page/(?P<page>\d+)/$', LatestTalksView.as_view(), name='latest-talks-paginated'),

    path('best', BestTalksView.as_view(), name='best-talks'),
    re_path(r'^best/page/(?P<page>\d+)/$', BestTalksView.as_view(), name='best-talks-paginated'),

    path('talk/<slug:slug>/', DetailTalkView.as_view(), name='talk-details'),
    path('talk/<slug:slug>/like', LikeTalkView.as_view(), name='talk-like'),
    path('talk/<slug:slug>/dislike', DislikeTalkView.as_view(), name='talk-dislike'),
    path('talk/<slug:slug>/favorite', FavoriteTalkView.as_view(), name='talk-favorite'),
    path('talk/<slug:slug>/watch', WatchTalkView.as_view(), name='talk-watch'),
]

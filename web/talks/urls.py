from django.urls import path
from django.urls import re_path
from django.urls import include

from django.views.generic import TemplateView

from .views import IndexView
from .views import LatestTalksView
from .views import BestTalksView
from .views import SearchTalksView
from .views import DetailTalkView
from .views import LikeTalkView
from .views import DislikeTalkView
from .views import FavoriteTalkView
from .views import DetailTagView
from .views import WatchTalkView
from .views import RSSLatestView

from rest_framework import routers

from .api import PlaylistViewSet
from .api import TalkViewSet
from .api import RandomTalkView

router = routers.DefaultRouter()
router.register(r'playlist', PlaylistViewSet)
router.register(r'talk', TalkViewSet)

app_name = 'talks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    path('rss/latest', RSSLatestView(), name='latest-feed'),

    path('latest', LatestTalksView.as_view(), name='latest-talks'),
    re_path(r'^latest/page/(?P<page>\d+)/$', LatestTalksView.as_view(), name='latest-talks-paginated'),

    path('best', BestTalksView.as_view(), name='best-talks'),
    re_path(r'^best/page/(?P<page>\d+)/$', BestTalksView.as_view(), name='best-talks-paginated'),

    path('search', SearchTalksView.as_view(), name='search'),

    path('talk/<slug:slug>/', DetailTalkView.as_view(), name='talk-details'),
    path('talk/<slug:slug>/like', LikeTalkView.as_view(), name='talk-like'),
    path('talk/<slug:slug>/dislike', DislikeTalkView.as_view(), name='talk-dislike'),
    path('talk/<slug:slug>/favorite', FavoriteTalkView.as_view(), name='talk-favorite'),
    path('talk/<slug:slug>/watch', WatchTalkView.as_view(), name='talk-watch'),

    path('tag/<slug:slug>/', DetailTagView.as_view(), name='tag-details'),
    path('tag/<slug:slug>/page/<int:page>/', DetailTagView.as_view(), name='tag-details-paginated'),

    path('api/', include(router.urls)),
    path('api/random-talk/', RandomTalkView.as_view(), name='random-talk')
]
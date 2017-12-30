from django.urls import path
from django.urls import re_path

from .views import IndexView

from .views import LatestTalksView
from .views import PopularTalksView

from .views import SearchTalksView

from .views import DetailTalkView

app_name = 'talks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('latest', LatestTalksView.as_view(), name='latest-talks'),
    re_path(r'^latest/page/(?P<page>\d+)/$', LatestTalksView.as_view(), name='latest-talks-paginated'),

    path('popular', PopularTalksView.as_view(), name='popular-talks'),
    re_path(r'^popular/page/(?P<page>\d+)/$', PopularTalksView.as_view(), name='popular-talks-paginated'),

    path('search', SearchTalksView.as_view(), name='search'),

    path('talk/<slug:slug>/', DetailTalkView.as_view(), name='talk-details'),
]
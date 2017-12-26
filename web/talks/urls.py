from django.urls import path
from django.urls import re_path

from .views import IndexView
from .views import LatestTalksView
from .views import SearchTalksView

app_name = 'talks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('latest', LatestTalksView.as_view(), name='latest-talks'),
    re_path(r'^latest/page/(?P<page>\d+)/$', LatestTalksView.as_view(), name='latest-talks-paginated'),
    path('search', SearchTalksView.as_view(), name='search'),
]
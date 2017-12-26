from django.urls import path
from django.urls import re_path

from .views import IndexView
from .views import LatestTalks
from .views import SearchView

app_name = 'talks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('latest', LatestTalks.as_view(), name='latest-talks'),
    re_path(r'^latest/page/(?P<page>\d+)/$', LatestTalks.as_view(), name='latest-talks-paginated'),
    # TODO
    # - Nice urls with search
    path('search', SearchView.as_view(), name='search'),
]
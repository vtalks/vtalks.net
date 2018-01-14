from django.urls import path
from django.urls import re_path
from django.urls import include

from tastypie.api import NamespacedApi

from .views import IndexView
from .views import LatestTalksView
from .views import BestTalksView
from .views import SearchTalksView
from .views import DetailTalkView
from .views import DetailTagView

from .api import ChannelResource
from .api import PlaylistResource
from .api import TalkResource

v1_api = NamespacedApi(api_name='v1', urlconf_namespace='talks')
v1_api.register(ChannelResource())
v1_api.register(PlaylistResource())
v1_api.register(TalkResource())

app_name = 'talks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('latest', LatestTalksView.as_view(), name='latest-talks'),
    re_path(r'^latest/page/(?P<page>\d+)/$', LatestTalksView.as_view(), name='latest-talks-paginated'),

    path('best', BestTalksView.as_view(), name='best-talks'),
    re_path(r'^best/page/(?P<page>\d+)/$', BestTalksView.as_view(), name='best-talks-paginated'),

    path('search', SearchTalksView.as_view(), name='search'),

    path('talk/<slug:slug>/', DetailTalkView.as_view(), name='talk-details'),

    path('tag/<slug:slug>/', DetailTagView.as_view(), name='tag-details'),
    path('tag/<slug:slug>/page/<int:page>/', DetailTagView.as_view(), name='tag-details-paginated'),

    path('api/', include(v1_api.urls)),
]
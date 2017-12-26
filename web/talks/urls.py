from django.urls import path

from .views import IndexView
from .views import LatestTalks
from .views import SearchView

app_name = 'talks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('latest', LatestTalks.as_view(), name='latest-talks'),
    path('search', SearchView.as_view(), name='search'),
]
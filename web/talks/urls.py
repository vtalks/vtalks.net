from django.urls import path

from .views import IndexView
from .views import SearchView

app_name = 'talks'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search', SearchView.as_view(), name='search'),
]
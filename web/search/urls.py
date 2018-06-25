from django.urls import path

from .views import SearchTalksView

app_name = 'search'
urlpatterns = [
    path('', SearchTalksView.as_view(), name='search'),
]

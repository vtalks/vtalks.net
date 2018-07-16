from django.urls import path

from .views import DetailTagView
from .views import TaggitAutocomplete

app_name = 'tags'
urlpatterns = [
    path('autocomplete/', TaggitAutocomplete.as_view(create_field='name'), name='tag-autocomplete'),

    path('<slug:slug>/', DetailTagView.as_view(), name='tag-details'),
    path('<slug:slug>/page/<int:page>/', DetailTagView.as_view(), name='tag-details-paginated'),
]
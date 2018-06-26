from django.urls import path

from .views import DetailTagView

app_name = 'tags'
urlpatterns = [
    path('<slug:slug>/', DetailTagView.as_view(), name='tag-details'),
    path('<slug:slug>/page/<int:page>/', DetailTagView.as_view(), name='tag-details-paginated'),
]
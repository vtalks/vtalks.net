from django.urls import path

from .views import DetailTopicView

app_name = 'topics'
urlpatterns = [
    path('<slug:slug>/', DetailTopicView.as_view(), name='topic-details'),
    path('<slug:slug>/page/<int:page>/', DetailTopicView.as_view(), name='topic-details-paginated'),
]
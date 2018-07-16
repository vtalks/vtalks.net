from django.urls import path

from .views import DetailTopicView
from .views import TopicListView

app_name = 'topics'
urlpatterns = [
    path('', TopicListView.as_view(), name='topic-list'),
    path('<slug:slug>/', DetailTopicView.as_view(), name='topic-details'),
    path('<slug:slug>/page/<int:page>/', DetailTopicView.as_view(), name='topic-details-paginated'),
]